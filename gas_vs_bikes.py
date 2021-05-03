import csv
import logging
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import requests
from collections import namedtuple, defaultdict, OrderedDict
import sys
from operator import attrgetter
import re

# Is there a relationship between the price of a gallon of gas (between 2019 and 2021) and
# frequency of ride-sharing (particularly, in this case ride-share Bike Rentals)?
# I did not find any statistically significant correlation between the two, however this may be
# because ride-share bikes are not are common as other means of ride-sharing and are extremely
# dependent upon weather and distance to travel

class Gas:

    def __init__(self, location, year, month, price):
        self.price = price
        self.month = month
        self.year = year
        self.location = location
        logging.debug('Gas initialized')

    def __repr__(self):
        return '%s, %d, %d, %f \n' % (self.location, self.year, self.month, self.price)

    def __str__(self):
        return '%s, %d, %d, %f \n' % (self.location, self.year, self.month, self.price)

    def __hash__(self):
        return hash((self.location, self.price, self.month, self.year))


class GasData:

    def __init__(self):
        self.gas_data = []
        GasData._load_data(self)
        logging.debug('GasData initialized')

    def __iter__(self):
        return iter(list(self.gas_data))

    def _load_data(self):
        #downloads file is it does not already exist
        logging.info('Entering _load_data in GasData')
        if not os.path.exists('gas_stats.txt'):
            self._get_data()
        Gas_Record = namedtuple('Gas_Record', 'series_id year period value footnote_codes')
        GasData._clean_data(self)
        #additional supporting file that contains area code interpretation
        url = 'https://download.bls.gov/pub/time.series/ap/ap.area'
        r = requests.get(url, allow_redirects=True, timeout=1)
        #write supporting file
        with open('area_codes.txt', 'wb') as f:
            f.write(r.content)
        logging.info('area_codes.txt successful download')
        #read cleaned file
        with open('gas_stats.clean.txt', 'r') as f, open('area_codes.txt', 'r') as a:
            reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
            read = csv.reader(a, delimiter='\t')
            area_codes = defaultdict(str)
            #this file is 2 columns: the code for city and the city's name
            for x in read:
                area_codes[x[0]] = x[1]
            #create namedtuples for each entry from cleaned file
            for row in reader:
                gas_record = Gas_Record(*row)
                #the 4-7 characters within 'series_id' are the code used for the city name
                l = gas_record.series_id[3:7]
                #the needed areas are the codes that are relevant to the cities being used in the study
                needed_areas = ['S11A', 'S12A', 'S12B', 'S23A', 'S23B', 'S24A', 'S24B', 'S35A', 'S35C', 'S49A', 'S49D', 'S49B', 'A315', 'A421', 'A425']
                if l not in needed_areas:
                    continue
                #there was no definitive code for Chattanooga between 2019 and 2021, the closest city code was used
                if l == 'S24B' or l == 'S35C':
                    location = 'Chattanooga'
                #there was no definitive code for Portand between 2019 and 2021, the closest city code was used
                elif l == 'S49D':
                    location = 'Portland'
                #there was no definitive code for Columbus between 2019 and 2021, the closest city code was used
                elif l == 'S23B':
                    location = 'Columbus'
                #only save entries which contain one of the needed_areas
                #split the name of the city
                else:
                    a = [val for key, val in area_codes.items() if l in key]
                    location = re.split('-', a[0])[0]
                year = int(float(gas_record.year))
                #ignore cases where the year was before 2019
                if year < 2019:
                    continue
                month = gas_record.period[1:]
                self.gas_data.append(Gas(location, year, int(month), round(float(gas_record.value), 2)))
        logging.info('gas_stats.clean.txt successful')

    def _get_data(self):
        logging.debug('Entering _get_data method')
        url = 'https://download.bls.gov/pub/time.series/ap/ap.data.2.Gasoline'
        r = requests.get(url, allow_redirects=True, timeout=1)
        with open('gas_stats.txt', 'wb') as f:
            f.write(r.content)
        logging.info('gas data successfully written')

    def _clean_data(self):
        logging.info('Entering _clean_data in GasData')
        with open('gas_stats.txt', 'r') as read, open('gas_stats.clean.txt', 'w') as write:
            reader = csv.reader(read)
            count = 0
            for line in reader:
                if count == 0:
                    count = 1
                    continue
                split_line = line[0].expandtabs(1)
                str_line = str(split_line).expandtabs()
                write.write(str_line)
                write.write('\n')
        logging.info('gas_stats.txt successfully cleaned')

    def price_over_time(self):
        #format month to be an integer based on its year where 01/2019 = 1, 01/2020 = 13, 01/2021 = 25
        #create dict with month integer as key and price during that month as item
        logging.debug('Entering price_over_time method')
        self.gas_data.sort(key=attrgetter('year', 'month', 'price'))
        price_dict = defaultdict(float)
        for x in self.gas_data:
            price = float(x.price)
            year = x.year
            month = x.month
            if year == 2020:
                month += 12
            if year == 2021:
                month += 24
            price_dict[month] = price
        logging.debug('price_over_time sucessful')
        return price_dict

    def price_frequency(self):
        #create dict where key is a range of gas prices, split evenly, and the item is
        # the sum of prices that fall in that range
        logging.debug('Entering price_frequency method')
        self.gas_data.sort(key=attrgetter('price'))
        price_dict = defaultdict(list)
        freq_dict = defaultdict(float)
        least = 0
        greatest = 0
        #keep track of the greatest value and the lowest value
        for y in self.gas_data:
            x = y.price
            if least == 0 and greatest == 0:
                least = x
                greatest = x
            elif x < least:
                least = x
            elif x > greatest:
                greatest = x
        #range between the greatest and least
        diff = greatest - least
        #divide the difference by an arbitrary number (in this case, 10), to attain ranges
        dev = diff/10.0
        while least <= greatest:
            #create lists of values that fall into each range
            for y in self.gas_data:
                x = y.price
                if least <= x < (least + dev):
                    price_dict[least].append(x)
                elif x == greatest:
                    price_dict[greatest].append(x)
            least += dev
        for key in price_dict:
            #create dict that counts the number of values for each range
            key_range = key
            freq_dict[key_range] = len(price_dict[key])
        sorted_freq_dict = sorted((float(x), y) for x, y in freq_dict.items())
        logging.debug('price_frequency successful')
        return sorted_freq_dict

    def price_per_city(self):
        #create dict that averages the price of gas per city
        logging.debug('Entering price_per_city method')
        self.gas_data.sort(key=attrgetter('location', 'price'))
        price_dict = defaultdict(list)
        avg_price_dict = defaultdict(float)
        for x in self.gas_data:
            #create lists that hold all prices with appropriate city
            location = x.location
            price = x.price
            price_dict[location].append(price)
        for x in price_dict:
            #average the prices in each city
            avg_price_dict[x] = round(sum(price_dict[x])/len(price_dict[x]), 2)
        logging.debug('price_per_city successful')
        return avg_price_dict


class Bike:

    def __init__(self, year, month, minutes, trips, location):
        self.month = month
        self.year = year
        self.minutes = minutes
        self.trips = trips
        self.location = location
        logging.debug('Bike initialized')

    def __repr__(self):
        return '%d, %d, %d, %d, %s \n' % (self.year, self.month, self.minutes, self.trips, self.location)

    def __str__(self):
        return '%d, %d, %d, %d, %s \n' % (self.year, self.month, self.minutes, self.trips, self.location)

    def __hash__(self):
        return hash((self.month, self.year, self.minutes, self.trips, self.location))


class BikeData:

    def __init__(self):
        self.bike_data = []
        BikeData._load_data(self)
        logging.debug('BikeData initialized')

    def __iter__(self):
        return iter(list(self.bike_data))

    def _load_data(self):
        #create file for data if it does not exist
        logging.info('Entering _load_data in BikeData')
        if not os.path.exists('bike_stats.txt'):
            self._get_data()
        #create namedtuples for each entry
        Bike_Record = namedtuple('Bike_Record', 'sysid sysname year assigned_month yr_mo_d sum_min num_trip sysname_alt')
        BikeData._clean_data(self)
        with open('bike_stats.clean.txt', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                bike_record = Bike_Record(*row)
                l = bike_record.sysname
                #parse the location name so that only the city is saved
                location = l[l.find('(')+1:l.find(',')]
                self.bike_data.append(Bike(int(bike_record.year), int(bike_record.assigned_month), int(bike_record.sum_min), int(bike_record.num_trip), location))
        logging.info('bike_stats.clean.txt successful')

    def _get_data(self):
        url = 'https://data.transportation.gov/api/views/g3h6-334u/rows.csv?accessType=DOWNLOAD'
        r = requests.get(url, allow_redirects=True, timeout=1)
        with open('bike_stats.txt', 'wb') as f:
            f.write(r.content)
        logging.info('bike data successfully written')

    def _clean_data(self):
        logging.info('Entering _clean_data in BikeData')
        with open('bike_stats.txt', 'r') as read, open('bike_stats.clean.txt', 'w') as write:
            reader = csv.reader(read)
            writer = csv.writer(write)
            count = 0
            for line in reader:
                if count == 0:
                    count = 1
                    continue
                writer.writerow(line)
        logging.info('bike_stats.txt successfully cleaned')

    def trips_over_time(self):
        #create dict to find the number of bike trips that were taken each month
        logging.debug('Entering trips_over_time method')
        self.bike_data.sort(key=attrgetter('year', 'month', 'trips'))
        trip_dict = defaultdict(int)
        for x in self.bike_data:
            year = x.year
            month = x.month
            trips = x.trips
            if year == 2020:
                month += 12
            if year == 2021:
                month += 24
            trip_dict[month] = trips
        logging.debug('trips_over_time sucessful')
        return trip_dict

    def trip_by_city(self):
        #create dict to sum the number of trips taken in each city
        logging.debug('Entering trip_by_city method')
        self.bike_data.sort(key=attrgetter('trips', 'location'))
        city_dict = defaultdict(list)
        sum_trips_dict = defaultdict(int)
        for x in self.bike_data:
            trips = x.trips
            location = x.location
            city_dict[location].append(trips)
        for x in city_dict:
            sum_trips_dict[x] = sum(city_dict[x])
        sum_trip = np.array(list(sum_trips_dict.items()))
        sorted_sum_trip = sum_trip[sum_trip[:, 0].argsort()]
        logging.debug('trip_by_city successful')
        return sorted_sum_trip

    def avg_length_trip(self):
        #create dict to find the average length of each bike trip taken per city
        logging.debug('Entering avg_length_trip method')
        self.bike_data.sort(key=attrgetter('location', 'minutes', 'trips'))
        trip_dict = defaultdict(float)
        for x in self.bike_data:
            location = x.location
            minutes = x.minutes
            trips = x.trips
            if trips == 0:
                continue
            avg_trip = float(minutes/trips)
            trip_dict[location] = avg_trip
        logging.debug('avg_length_trip successful')
        return trip_dict


def main():

    #initialize logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #set level to the console
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    #set level to a file
    fh = logging.FileHandler('gas_vs_bikes.log', mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    #argparse to read command line
    parser = argparse.ArgumentParser(description='This is a description of my parser')
    parser.add_argument('command', metavar='<print>', choices=['print'], help='make sure to print')
    #parser.add_argument('-o', '--ofile', dest='output', metavar='<outfile>', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='choose your output method')

    args = parser.parse_args()
    #output = str(args.output)
    # if output.__contains__('stdout'):
    #     output = sys.stdout
    # else:
    #     output = output.split(' ')[2]
    #     output = output.strip("',")

    gas = GasData()
    bike = BikeData()
    #create variables for each data set
    gas_over_time_data = GasData.price_over_time(gas)
    bike_over_time_data = BikeData.trips_over_time(bike)
    bike_per_city_data = BikeData.trip_by_city(bike)
    gas_price_frequency_data = GasData.price_frequency(gas)
    avg_length_trip_data = BikeData.avg_length_trip(bike)
    avg_city_price_data = GasData.price_per_city(gas)

    #create numpy array to compare the price of gas over time vs the number of bike rentals over time
    gas_vs_bike_data = OrderedDict()
    for m in range(len(gas_over_time_data)):
        g = gas_over_time_data.get(m)
        b = bike_over_time_data.get(m)
        gas_vs_bike_data[g] = b
    gas_time_plot_points = np.array(list(gas_vs_bike_data.items()))
    sorted_gas_time = gas_time_plot_points[gas_time_plot_points[:, 0].argsort()]
    logging.info('gas_vs_bike_data successful')

    #create numpy array to compare the average length of each trip per city with the average price of gas in each city
    len_per_price_data = defaultdict(float)
    for m in avg_length_trip_data:
        if m in avg_city_price_data:
            len_per_price_data[avg_length_trip_data[m]] = avg_city_price_data[m]
        elif m == 'Jersey City':
            len_per_price_data[avg_length_trip_data[m]] = avg_city_price_data['New York']
    len_per_trip_points = np.array(list(len_per_price_data.items()))
    sort_len_per_trip = len_per_trip_points[len_per_trip_points[:, 0].argsort()]
    logging.info('len_per_trip successful')

    #create a numpy array to compare the range of gas prices with the number of bike rentals
    trips_per_freq = defaultdict(list)
    avg_trip_freq = defaultdict(float)
    temp = []
    for x in gas_price_frequency_data:
        temp.append(x[0])
    for n in gas_vs_bike_data:
        for m in range(len(gas_price_frequency_data)):
            low_freq = round(temp[m], 2)
            hi_freq = 0
            if m < len(temp) - 1:
                hi_freq = temp[m+1]
            if low_freq <= n < hi_freq:
                trips_per_freq[low_freq].append(gas_vs_bike_data[n])
            elif n == hi_freq:
                trips_per_freq[hi_freq].append(gas_vs_bike_data[n])
    for x in trips_per_freq:
        avg_trip_freq[x] = sum(trips_per_freq[x])/len(trips_per_freq[x])
    avg_trip_freq_points = np.array(list(avg_trip_freq.items()))
    sort_avg_trip_freq = avg_trip_freq_points[avg_trip_freq_points[:, 0].argsort()]
    logging.info('avg_trip_freq successful')

    #save all the calculated data to a single csv file
    with open('gas_vs_bike_data.txt', 'w') as f:
        write = csv.writer(f)
        write.writerow('Price of Gas Over Time')
        for x in gas_over_time_data:
            write.writerow([x, gas_over_time_data[x]])
        write.writerow('\n\n')
        write.writerow('Number of Bike trips Over Time')
        for x in bike_over_time_data:
            write.writerow([x, bike_over_time_data[x]])
        write.writerow('\n\n')
        write.writerow('Number of Bike Rentals per City')
        for x in bike_per_city_data:
            write.writerow([x])
        write.writerow('\n\n')
        write.writerow('Frequency of Gas Prices')
        for x in gas_price_frequency_data:
            write.writerow([x])
        write.writerow('\n\n')
        write.writerow('Average Length of Bike Trips Per City')
        for x in avg_length_trip_data:
            write.writerow([x, avg_length_trip_data[x]])
        write.writerow('\n\n')
        write.writerow('Average Price of Gas Per City')
        for x in avg_city_price_data:
            write.writerow([x, avg_city_price_data[x]])
        write.writerow('\n\n')
        write.writerow('Bike Rentals by Gas Price')
        for x in sorted_gas_time:
            write.writerow(x)
        write.writerow('\n\n')
        write.writerow('Average Length of Each Trip Per City by Price Per City')
        for x in sort_len_per_trip:
            write.writerow(x)
        write.writerow('\n\n')
        write.writerow('Average Bike Trips Per Range of Gas Prices')
        for x in sort_avg_trip_freq:
            write.writerow(x)
    logging.info('csv successfully written')

    #create x and y variables for each plot
    x1axis = [x for x in gas_over_time_data]
    y1axis = [gas_over_time_data[x] for x in gas_over_time_data]

    x2axis = []
    y2axis = []
    for m in gas_price_frequency_data:
        x2axis.append(m[0])
        y2axis.append(m[1])

    x3axis = [x for x in avg_city_price_data]
    y3axis = [avg_city_price_data[x] for x in avg_city_price_data]

    x4axis = [x for x in bike_over_time_data]
    y4axis = [bike_over_time_data[x] for x in bike_over_time_data]

    x5axis = [x for x in avg_length_trip_data]
    y5axis = [avg_length_trip_data[x] for x in avg_length_trip_data]

    x6axis = bike_per_city_data[:, 0]
    y6axis = bike_per_city_data[:, 1]

    x7axis = sorted_gas_time[:, 0]
    y7axis = sorted_gas_time[:, 1]

    x8axis = sort_len_per_trip[:, 0]
    y8axis = sort_len_per_trip[:, 1]

    x9axis = sort_avg_trip_freq[:, 0]
    y9axis = sort_avg_trip_freq[:, 1]
    logging.debug('plot points sucessful')

    months = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    #Figure 1 shows 2 plots:
    # - Gas prices over time
    # - Bike rentals over time
    fig1, axs = plt.subplots(2)

    axs[0].plot(x1axis, y1axis)
    axs[0].set_title('Gas Prices Over Time')
    axs[0].set_xlabel('Month from Jan, 2019')
    axs[0].set_ylabel('Price per Gallon of Gas')
    axs[0].set(xlim=(1, 25))
    axs[1].plot(x4axis, y4axis)
    axs[1].set_title('Bike Rentals Over Time')
    axs[1].set_xlabel('Months from Jan, 2019')
    axs[1].set_ylabel('Number of Bike Rentals')
    axs[1].set(xlim=(1, 25))

    #Figure 2 shows 3 plots:
    # - Avg gas price per city
    # - Avg price per gallon of gas
    # - Avg length of bike trip per city
    fig2, axs = plt.subplots(3)

    axs[0].bar([x for x in range(len(x3axis))], y3axis)
    axs[0].set_title('Average Gas Price Per City')
    axs[0].set_xticklabels(x3axis)
    axs[0].set_xlabel('City')
    axs[0].set_ylabel('Average Price per Gallon of Gas')
    axs[1].bar([x for x in range(len(x5axis))], y5axis)
    axs[1].set_title('Average Trip Length Per City')
    axs[1].set_xticklabels(x5axis)
    axs[1].set_xlabel('City')
    axs[1].set_ylabel('Average Length of Trip')

    axs[2].plot([x for x in range(len(x6axis))], y6axis)
    axs[2].set_title('Bike Trips Per City')
    axs[2].set_xticklabels(x6axis)
    axs[2].set_xlabel('City')
    axs[2].set_ylabel('Number of Trips')

    #Figure 3 shows 2 plots:
    # - Freq of gas prices
    # - Avg number of bike trips per range of gas price
    fig3, axs = plt.subplots(2)

    axs[0].bar([x for x in range(len(x2axis))], y2axis, align='edge')
    axs[0].set_title('Frequency Of Gas Prices')
    axs[0].set_xticklabels(x2axis)
    axs[0].set_xlabel('Price Range')
    axs[0].set_ylabel('Frequency of Price Range')

    axs[1].bar([x for x in range(len(x9axis))], y9axis, align='edge')
    axs[1].set_title('Average Number of Bike trips Per Range of Gas Price')
    axs[1].set_xticklabels(x9axis)
    axs[1].set(ylim=(50000, 100000))
    axs[1].set_xlabel('Price Range')
    axs[1].set_ylabel('Number of Bike Trips')

    #Figure 4 shows 2 plots:
    # - Gas prices vs bike rentals
    # - Avg length of bike trip by gas price
    fig4, axs = plt.subplots(2)

    axs[0].plot(x7axis, y7axis)
    axs[0].set_title('Gas Prices vs Bike Rentals')
    axs[0].set_xlabel('Price Per Gallon of Gas')
    axs[0].set_ylabel('Number of Bike Rentals')

    axs[1].plot(x8axis, y8axis)
    axs[1].set_title('Average Length per Bike Trip by Gas Price')
    axs[1].set_xlabel('Average Length of Bike Trip Per City')
    axs[1].set_ylabel('Average Price per Gallon of Gas Per City')

    plt.show()
    fig1.savefig('Gas_Bike_Time.jpg')
    fig2.savefig('Gas_Bike_Avgs.jpg')
    fig3.savefig('Gas_Bike_Freq.jpg')
    fig4.savefig('Gas_vs_bike.jpg')


if __name__ == '__main__':
    main()
