import csv
import sys
from collections import namedtuple
from operator import attrgetter
import os
import logging
import argparse
import requests
from collections import defaultdict
import matplotlib.pyplot as plt


class AutoMPG:

    def __init__(self, make, model, year, mpg):
        self.make = make
        self.model = model
        self.year = year
        self.mpg = mpg
        logging.debug("AutoMPG initialized")

    def __repr__(self):
        return '%s %s 19%s %s \n' % (self.make, self.model, self.year, self.mpg)

    def __str__(self):
        return '%s %s 19%s %s \n' % (self.make, self.model, self.year, self.mpg)

    def __eq__(self, other):
        logging.debug("Entering __eq__ method")

        if type(self) == type(other):
            logging.debug("__eq__ successful")
            return self.make == other.make and self.model == other.model and self.year == other.year and self.mpg == other.mpg
        else:
            logging.info('__eq__ unsuccessful')
            return NotImplemented

    def __lt__(self, other):
        logging.debug("Entering __lt__ method")

        if type(self) == type(other):
            logging.debug("__lt__ successful")
            return (self.make, self.model, self.year, self.mpg) < (other.make, other.model, other.year, other.mpg)

        else:
            logging.info('__lt__ unsuccessful')
            return NotImplemented

    def __hash__(self):
        return hash((self.make, self.model, self.year, self.mpg))


class AutoMPGData:

    def __init__(self):
        self.data = []
        AutoMPGData._load_data(self)
        logging.debug("AutoMPGData initialized")

    def __iter__(self):
        return iter(list(self.data))

    def _load_data(self):
        logging.info("Entering _load_data method")
        if not os.path.exists("auto-mpg.clean.txt"):
            self._get_data()
        Record = namedtuple("Record", "mpg cylinders displacement horsepower weight acceleration model_year origin car_name")
        AutoMPGData._clean_data(self)
        with open("auto-mpg.clean.txt", "r") as f:
            reader = csv.reader(f, skipinitialspace=True, delimiter=' ')
            #loop through each line
            for row in reader:
                #create namedtuple
                record = Record(*row)
                #split the car_name tuple value into 2
                make_model = record.car_name.split()
                #assign value "make" to the first split value
                make = make_model[0]
                if make == 'chevroelt' or make == 'chevy':
                    make = 'chevrolet'
                elif make == 'maxda':
                    make = 'mazda'
                elif make == 'mercedes-benz':
                    make = 'mercedes'
                elif make == 'toyouta':
                    make = 'toyota'
                elif make == 'vokswagen'or make == 'vw':
                    make = 'volkswagen'

                #for make_model values that are more than one word,
                #add the subsequent words together to create the model
                if len(make_model) > 1:
                    model = make_model[1]
                if len(make_model) > 2:
                    model += ' ' + make_model[2]
                if len(make_model) > 3:
                    model += ' ' + make_model[3]
                #add the data to list
                self.data.append(AutoMPG(make, model, record.model_year, record.mpg))
            logging.info("auto-mpg.clean.txt read successful")

    def _clean_data(self):
        logging.info("Entering _clean_data method")
        with open("auto-mpg.data.txt", "r") as read, open("auto-mpg.clean.txt", "w") as write:
            reader = csv.reader(read)
            for line in reader:
                split_line = line[0].expandtabs(1)
                str_line = str(split_line).expandtabs()
                write.write(str_line)
                write.write('\n')
            logging.info("read auto-mpg.data.txt, wrote auto-mpg.clean.txt successful")

    def sort_by_default(self):
        logging.info("Entering sort_by_default method")
        self.data.sort()
        logging.info("Default sort successful")
        #AutoMPGData.mpg_by_make(self)

    def sort_by_year(self):
        logging.info("Entering sort_by_year method")
        self.data.sort(key=attrgetter('year', 'make', 'model', 'mpg'))
        logging.info("Year sort successful")
        #AutoMPGData.mpg_by_year(self)

    def sort_by_mpg(self):
        logging.info("Entering sort_by_mpg method")
        self.data.sort(key=attrgetter('mpg', 'make', 'model', 'year'))
        logging.info("mpg sort successful")

    def _get_data(self):
        url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
        r = requests.get(url, allow_redirects=True, timeout=0.2)
        with open('auto-mpg.data.txt', 'wb') as f:
            f.write(r.content)
        logging.info('data retrieved successful')

    def mpg_by_year(self):
        mpg_dict = defaultdict(list)
        avg_mpg_dict = defaultdict(float)
        for x in self.data:
            mpg = float(x.mpg)
            year = '19' + x.year
            mpg_dict[year].append(mpg)
        for key in mpg_dict:
            avg_mpg_dict[key] = sum(mpg_dict[key])/len(mpg_dict[key])
        return avg_mpg_dict

    def mpg_by_make(self):
        mpg_dict = defaultdict(list)
        avg_mpg_dict = defaultdict(float)
        for x in self.data:
            mpg = float(x.mpg)
            make = x.make
            mpg_dict[make].append(mpg)
        for key in mpg_dict:
            avg_mpg_dict[key] = sum(mpg_dict[key]) / len(mpg_dict[key])
        return avg_mpg_dict


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
    fh = logging.FileHandler('autompg2.log', mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    #argparse to read command line
    parser = argparse.ArgumentParser(description='This is a description of my parser')
    parser.add_argument('command', metavar='<print>', choices=['print'], help='make sure to print')
    parser.add_argument('-s', '--sort', dest='sort', action='store', metavar='<sort choice>', choices=['year', 'mpg', 'default'], required=True, help='choose your sort order')
    parser.add_argument('-o', '--ofile', dest='output', metavar='<outfile>', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='choose your output method')
    parser.add_argument('-p', '--plot', dest='plot', action='store_true')
    parser.add_argument('-m', dest='mpg_by', metavar='<mpg_by>', action='store', choices=['year', 'make'])

    args = parser.parse_args()
    sort_type = args.sort
    print(sort_type)
    output = str(args.output)
    if output.__contains__('stdout'):
        output = sys.stdout
    else:
        output = output.split(' ')[2]
        output = output.strip("',")
    plot = args.plot
    mpg_avg = args.mpg_by

    auto = AutoMPGData()
    if mpg_avg == 'year':
        data = AutoMPGData.mpg_by_year(auto)
    elif mpg_avg == 'make':
        data = AutoMPGData.mpg_by_make(auto)

    if mpg_avg == 'year' or mpg_avg == 'make':
        with open('mpg_avgs.txt', 'w') as f:
            wr = csv.writer(f, delimiter='\t')
            for x in data:
                wr.writerow([x, data[x]])

    if plot and (mpg_avg == 'year' or mpg_avg == 'make'):
        xaxis = [x for x in data]
        yaxis = [data[x] for x in data]
        plt.xlabel(mpg_avg)
        plt.ylabel('MPG')
        xsize = range(len(xaxis))
        plt.xticks(xsize, xaxis)
        plt.plot(xsize, yaxis, 'o')
        plt.title('Average MPG by ' + mpg_avg)
        plt.show()
        plt.savefig('MPG_plot.jpg')

    #using arg to determine sort choice
    if sort_type == 'default':
        #sorting data by default method
        logging.info('sorting by default')
        AutoMPGData.sort_by_default(auto)

    elif sort_type == 'mpg':
        #sorting data by mpg method
        logging.info('sorting my mpg')
        AutoMPGData.sort_by_mpg(auto)

    elif sort_type == 'year':
        #sorting method by year method
        logging.info('sorting by year')
        AutoMPGData.sort_by_year(auto)

    with open(output, 'w') if output != 'sys.stdout' else sys.stdout as f:
        wr = csv.writer(f, delimiter='\t')
        wr.writerow(auto.data)


if __name__ == "__main__":
    main()

