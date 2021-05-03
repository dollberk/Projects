using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using BlueSkies;

public class WeatherCreator : MonoBehaviour
{

    //UI fields
    public Dropdown PrecipitationDropDown;
    public Slider PrecipIntensitySlider;
    public Dropdown CloudCoverageDropDown;
    public Dropdown WindDirectionDropDown;
    public InputField WindSpeedInput;
    public InputField SystemSpeedInput;
    public InputField SystemRadiusInput;
    public Slider FogSlider;
    public InputField YearInput;
    public InputField MonthInput;
    public InputField DayInput;
    public InputField HourInput;
    public InputField MinuteInput;
    public InputField SecondInput;
    public Dropdown TimeZoneDropDown;
    public Slider TimeOfDaySlider;
    public InputField ATRInput;
    public InputField LatitudeInput;
    public InputField LongitudeInput;
    public InputField AltitudeInput;
    public Toggle DaylightSavings;


    //precipitation & destroy container game objects
    public GameObject Rain;
    public GameObject Snow;
    public GameObject Sleet;
    public GameObject Cumulus;
    public GameObject Cirrus;
    public GameObject Stratus;
    private IPrecipitationManager precipitationManager = null;
    private GameObject PrecipitationContainer;
    private GameObject BlueSkiesContainer;
    private GameObject CloudsContainer;
    public string precipIntensity;
    public ulong precipID;
    Precipitation precipitation = null;

    //cloud & cloud layers type
    private ICloudManager cloudManager = null;
    ICloudLayer cloudLayer = new CloudLayer();
    ISilverLining silverLining = new SilverLining();
    public CloudType type;
    private List<ulong> CloudIDList;
    private List<ulong> CloudLayerIDList;
    public ulong fogID;
    public bool activeFog;
    public float someFog;

    //wind layers direction & speed
    public IWindManager windManager = null;
    public float windDirection;
    public float windSpeed;
    private List<ulong> WindIDList;

    //weather system movement speed & size
    public float systemSpeed;
    public float systemRadius;
    public List<(string, ulong)> systemAspectList;

    //time of date & current time
    public int timeOfDay;
    public float timeZone;
    System.DateTime currentTime = System.DateTime.UtcNow;
    IBlueSkiesTime blueSkiesTime = new BlueSkiesTime();
    public int year;
    public int month;
    public int day;
    public int hour;
    public int minute;
    public int seconds;
    public bool daylightSavingsOn;
    public double latitude;
    public double longitude;
    public double altitude;
    //public int time;
    //public float advanceTimeRate;
    //public bool advanceTimeRateBool;

    //ListBox button display text
    public string precipName;
    public string cloudName;
    public string windName;
    public string textString;

    //Slider display text
    public Text textTimeSliderValue;
    public Text textFogSliderValue;
    public Text textPrecipSliderValue;

    //ListBox button creation
    public Button addSystemButton;
    public GameObject buttonPrefab;


    void Start()
    {
        cloudManager = BlueSkiesManager.Instance().CloudManager;
        CloudIDList = new List<ulong>();
        CloudLayerIDList = new List<ulong>();
        windManager = BlueSkiesManager.Instance().WindManager;
        WindIDList = new List<ulong>();
        precipitationManager = BlueSkiesManager.Instance().PrecipitationManager;
        Button btn = addSystemButton.GetComponent<Button>();
        btn.onClick.AddListener(addWeatherSystem);
        //timeZone = -4;
        BlueSkiesContainer = BlueSkiesManager.Instance().transform.parent.gameObject;
        PrecipitationContainer = BlueSkiesContainer.transform.Find("Precipitation").gameObject;
        CloudsContainer = BlueSkiesContainer.transform.Find("Clouds").gameObject;

        //These are for us, now that we are instantiating the weather effects ourselves
        Rain = ObjectsUtil.FindGameObject(PrecipitationContainer, "PrecipitationRain_OverCamera");
        Sleet = ObjectsUtil.FindGameObject(PrecipitationContainer, "PrecipitationSleet_OverCamera");
        Snow = ObjectsUtil.FindGameObject(PrecipitationContainer, "PrecipitationSnow_OverCamera");
        Cumulus = ObjectsUtil.FindGameObject(PrecipitationContainer, "CumulusClouds");
        Cirrus = ObjectsUtil.FindGameObject(PrecipitationContainer, "CirrusClouds");
        Stratus = ObjectsUtil.FindGameObject(PrecipitationContainer, "StratusClouds");
        //updateDayTime();
    }

    private void Update()
    {
        //updateTime();
        if (Input.GetKeyDown("w"))
        {
            DeleteClouds();
        }

        if (Input.GetKeyDown("d"))
        {
            DeleteWind();
        }
    }
    /// <summary>
    /// Update methods
    /// </summary>

    public void UpdatePrecipitation()
    {
        //set precipitation type

        switch (PrecipitationDropDown.value)
        {
            case 0:
                //None
                Rain.SetActive(false);
                Snow.SetActive(false);
                Sleet.SetActive(false);
                precipName = "NONE";
                break;

            case 1:
                //Rain
                Rain.SetActive(true);
                Snow.SetActive(false);
                Sleet.SetActive(false);
                precipName = "Rain";
                break;

            case 2:
                //Sleet
                Sleet.SetActive(true);
                Rain.SetActive(false);
                Snow.SetActive(false);
                precipName = "Sleet";
                break;

            case 3:
                //Snow
                Snow.SetActive(true);
                Rain.SetActive(false);
                Sleet.SetActive(false);
                precipName = "Snow";
                break;
        }
        precipID = silverLining.getNewUID();
        Debug.Log(precipID);
    }

    public void UpdatePrecipIntensity()
    {
        if (PrecipIntensitySlider.value != 0)
        {
            precipIntensity = PrecipIntensitySlider.value + "";
            textPrecipSliderValue.text = precipIntensity + "/30";


            //////////////////////////Make work
            
            //precip.GetComponent<ParticleSystem>();
            //var emission = precip.emission;
            //emission.rateOverTime = PrecipIntensitySlider.value;

            //BlueSkiesManager.Instance().PrecipitationManager.setPrecipitationIntensity(PrecipIntensitySlider.value);
        }
    }

    public void UpdateCloudCoverage()
    {
        //set cloud type
        switch (CloudCoverageDropDown.value)
        {
            case 0:
                //No Clouds
                DeleteClouds();
                cloudName = " ";
                break;

            case 1:
                //Cumulus Congestus Layer
                //No storm
                cloudName = "Cumulus Congestus";
                addCloudLayer(CloudType.CUMULUS_CONGESTUS, new Vector3(0f, 900f, 0f), new Vector3(30000f, 0f, 30000f), true, 2f, 2750);
                break;

            case 2:
                // Single Cumulus Congestus Cloud
                addCloud(CloudType.CUMULUS_CONGESTUS, new Vector3(3000f, 5000f, 0f), 9000, new Vector3(4000f, 1000f, 4000f));
                cloudName = "Cumulus";
                break;


            case 3:
                //Cumulus Mediocris Layer
                //No storm
                cloudName = "Cumulus Mediocris";
                addCloudLayer(CloudType.CUMULUS_MEDIOCRIS, new Vector3(0f, 900f, 0f), new Vector3(30000f, 0f, 30000f), true, 1.0f, 2750);
                break;

            case 4:
                //Single Cumulus Mediocris Cloud
                addCloud(CloudType.CUMULUS_MEDIOCRIS, new Vector3(3000f, 5000f, 0f), 9000, new Vector3(4000f, 1000f, 4000f));
                cloudName = "Cumulus Mediocris";
                break;

            case 5:
                //Cumulonimbus Layer
                //Thunderstorm
                cloudName = "Cumulonimbus";
                addCloudLayer(CloudType.CUMULONIMBUS, new Vector3(0f, 900f, 0f), new Vector3(30000f, 0f, 30000f), true, 1.0f, 2750);
                break;

            case 6:
                //Single Cumulonimbus Cloud
                addCloud(CloudType.CUMULONIMBUS, new Vector3(3000f, 5000f, 0f), 9000, new Vector3(4000f, 1000f, 4000f));
                cloudName = "Cumulonimbus";
                break;

            case 7:
                //Stratocumulus Layer
                //No/light precip
                //low altitude/horizontal coverage
                cloudName = "Stratocumulus";
                addCloudLayer(CloudType.STRATOCUMULUS, new Vector3(0f, 900f, 0f), new Vector3(30000f, 0f, 30000f), true, 1.0f, 2750);
                break;

            case 8:
                //Single Stratocumulus Cloud
                addCloud(CloudType.STRATOCUMULUS, new Vector3(3000f, 5000f, 0f), 9000, new Vector3(4000f, 1000f, 4000f));
                cloudName = "Stratocumulus";
                break;

            case 9:
                //Stratus Layer
                //No/light precip
                //low altitude/horizontal coverage
                cloudName = "Stratus";
                addCloudLayer(CloudType.STRATUS, new Vector3(0f, 900f, 0f), new Vector3(30000f, 0f, 30000f), true, 1.0f, 2750);
                break;

            case 10:
                //Single Stratus Cloud
                addCloud(CloudType.STRATUS, new Vector3(3000f, 5000f, 0f), 9000, new Vector3(4000f, 1000f, 4000f));
                cloudName = "Stratus";
                break;

            case 11:
                //Cirrus Layer
                //high altitude
                cloudName = "Cirrus";
                addCloudLayer(CloudType.CIRRUS, new Vector3(0f, 900f, 0f), new Vector3(30000f, 0f, 30000f), true, 1.0f, 2750);
                break;

            case 12:
                //Single Cirrus Cloud
                addCloud(CloudType.CIRRUS, new Vector3(3000f, 5000f, 0f), 9000, new Vector3(4000f, 1000f, 4000f));
                cloudName = "Cirrus";
                break;
        }
    }


    /*private void setFogRendering(float fogDensity, Color fogColor)
    {
        RenderSettings.fog = activeFog;
        RenderSettings.fogDensity = fogDensity;
        RenderSettings.fogColor = fogColor;
    }

    public void addFog()
    {
        //fog toggle & set density
        someFog = string.Format("{0:0.000}", FogSlider.value);
        if (FogSlider.value != 0)
        {
            textFogSliderValue.text = someFog + "/1.000";
            addCloudLayer(CloudType.VOLUMETRIC_FOG, new Vector3(0f, 0f, 0f), new Vector3(30000f, 30f, 30000f), true, FogSlider.value, 2750);
        }
        else
        {
            destroyOneCloudLayer(fogID);
        }
    }*/

    /*public void ShowFogSliderValue()
    {
        //creates text to display value on sliders
        string sliderMessage = "";
    
    
          if (FogSlider.value == 0)
          {
              sliderMessage = "No Fog";
          }
          else if (FogSlider.value < 0.35)
          {
              sliderMessage = "Low Density";
          }
          else if (FogSlider.value < 0.65)
          {
              sliderMessage = "Medium Density";
          }
          else
          {
              sliderMessage = "High Density";
          }
    
        FogValue.text = string.Format("{0:0.000}", FogSlider.value) + " " + sliderMessage;
    }*/

    public void UpdateWindDirection()
    {
        //set wind direction
        switch (WindDirectionDropDown.value)
        {
            case 0:
                //None
                windSpeed = 0;
                DeleteWind();
                windName = " ";
                break;

            case 1:
                //North
                windDirection = 0;
                windName = "N";
                break;

            case 2:
                //North northeast
                windDirection = 22.5f;
                windName = "NNE";
                break;

            case 3:
                //Northeast
                windDirection = 45;
                windName = "NE";
                break;

            case 4:
                //East northeast
                windDirection = 67.5f;
                windName = "ENE";
                break;

            case 5:
                //East
                windDirection = 90;
                windName = "E";
                break;

            case 6:
                //East southeast
                windDirection = 112.5f;
                windName = "ESE";
                break;

            case 7:
                //Southeast
                windDirection = 135;
                windName = "SE";
                break;

            case 8:
                //South southeast
                windDirection = 157.5f;
                windName = "SSE";
                break;

            case 9:
                //South
                windDirection = 180;
                windName = "S";
                break;

            case 10:
                //South southwest
                windDirection = 202.5f;
                windName = "SSW";
                break;

            case 11:
                //Southwest
                windDirection = 225;
                windName = "SW";
                break;

            case 12:
                //West southwest
                windDirection = 247.5f;
                windName = "WSW";
                break;

            case 13:
                //West
                windDirection = 270;
                windName = "W";
                break;

            case 14:
                //West northwest
                windDirection = 292.5f;
                windName = "WNW";
                break;

            case 15:
                //Northwest
                windDirection = 315;
                windName = "NW";
                break;
            case 16:
                //North northwest
                windDirection = 337.5f;
                windName = "NNW";
                break;

        }
        CreateWind();
    }

    public void UpdateWindSpeed()
    {
        //set wind speed
        if (WindSpeedInput.text == null)
        {
            windSpeed = 0;
        }
        else
        {
            windSpeed = float.Parse(WindSpeedInput.text);
        }

    }

    /* public void UpdateSystemSpeed() //Needs more work
    {
        //set system speed
        if (SystemSpeedInput.text != null)
        {
            systemSpeed = float.Parse(SystemSpeedInput.text);
        }
        else
        {
            systemSpeed = 0;
        }
        if (CloudCoverageDropDown.value != 0)
        {

            //ICloud Cloud = BlueSkiesManager.Instance().CloudManager.getCloud(CloudIDList[CloudIDList.Count - 1]);
            //ICloudLayer CloudLayer = BlueSkiesManager.Instance().CloudManager.getCloudLayer(CloudLayerIDList[CloudLayerIDList.Count - 1]);
            //BlueSkiesManager.Instance().WindManager.moveCloud(Cloud);
            //BlueSkiesManager.Instance().WindManager.moveCloudLayer(CloudLayer);

        }

        if (PrecipitationDropDown.value != 0)
        {

        }
    }

    public void UpdateSystemRadius()
    {
        //set system size
        if (SystemRadiusInput.text != null)
        {
            systemRadius = float.Parse(SystemRadiusInput.text);
        }
        else
        {
            //random set radius
            systemRadius = 10000;
        }

        if (PrecipitationDropDown.value != 0)
        {
            precipitation.setEffectRange(0.0f, 0.0f, false);

            partpart = GetComponent<ParticleSystem>();
            var sh = part.shape;
            sh.scale = new Vector3(x, y, z);
        }
    }*/

    public void updateDateTime()
    {

        if (YearInput.text == "" || MonthInput.text == "" || DayInput.text == "")
        {
            useCurrentTime();
        }
        else
        {
            year = int.Parse(YearInput.text);
            month = int.Parse(MonthInput.text);
            day = int.Parse(DayInput.text);
        }


        BlueSkiesManager.Instance()._year = year;
        BlueSkiesManager.Instance()._month = month;
        BlueSkiesManager.Instance()._day = day;
        updateDaylightSavings();
        BlueSkiesManager.Instance().TimeManager.setDate(year, month, day);
        BlueSkiesManager.Instance().TimeManager.GetEpoch2000Centuries(true);
    }

    public void updateTimeOfDay()
    {

        if (HourInput.text == "" || MinuteInput.text == "" || SecondInput.text == "")
        {
            hour = 12;
            minute = 0;
            seconds = 0;
        }
        else
        {
            hour = int.Parse(HourInput.text);
            minute = int.Parse(MinuteInput.text);
            seconds = int.Parse(SecondInput.text);
        }
        //timeOfDay = (int)TimeOfDaySlider.value;
        //textTimeSliderValue.text = timeOfDay + ":00";
        BlueSkiesManager.Instance()._hour = hour;
        BlueSkiesManager.Instance()._minute = minute;
        BlueSkiesManager.Instance()._seconds = seconds;
        BlueSkiesManager.Instance().TimeManager.setTime(hour, minute, seconds, timeZone, daylightSavingsOn);
    }

    public void useCurrentTime()
    {
        string time = currentTime.ToString();
        string[] timeArray = time.Split(new char[] { '/', ' ', ':' });
        try
        {
            month = System.Int32.Parse(timeArray[0]);
            day = System.Int32.Parse(timeArray[1]);
            year = System.Int32.Parse(timeArray[2]);
        }
        catch
        {
            Debug.Log("Cannot parse current date");
        }
    }




    /*public void updateDateTime2() //Not currently in use
    {
        //set current computer time & chosen time of day
        string time = currentTime.ToString();
        string[] timeArray = time.Split(new char[] { '/', ' ', ':' });
        try
        {
            month = System.Int32.Parse(timeArray[0]);
            day = System.Int32.Parse(timeArray[1]);
            year = System.Int32.Parse(timeArray[2]);
        }
        catch
        {
            Debug.Log("Cannot parse current date");
        }
        //Debug.Log("month = " + month + ", Day = " + day + ", Year= " + year);
        blueSkiesTime.setDate(year, month, day);
        timeOfDay = (int)TimeOfDaySlider.value;
        textTimeSliderValue.text = TimeOfDaySlider.value + ":00";
        blueSkiesTime.setTime(timeOfDay, 0, 0, timeZone, false);
        silverLining.setTime(year, month, day, timeOfDay, 0, 0, timeZone, false);
        silverLining.getMoonDay(year, month, day);
        BlueSkiesManager.Instance().TimeManager.setDate(year, month, day);
        BlueSkiesManager.Instance().TimeManager.GetEpoch2000Centuries(true);
        BlueSkiesManager.Instance().TimeManager.setTime(timeOfDay, 0, 0, timeZone, true);
        //Debug.Log(timeZone);
    }*/

    public void updateTimeZone()
    {
        //set timezone based on GMT
        switch (TimeZoneDropDown.value)
        {
            case 0:
                //Default EST
                timeZone = -5;
                break;

            case 1:
                //EST
                timeZone = -5;
                break;

            case 2:
                //CST
                timeZone = -6;
                break;

            case 3:
                //MST
                //Arizona does not use daylight savings
                //approximate lat/longs
                if (latitude > 32 && latitude < 37 && longitude < -109 && longitude > -114)
                {
                    daylightSavingsOn = false;
                }
                timeZone = -7;
                break;

            case 4:
                //PST
                timeZone = -8;
                break;

            case 5:
                //AST
                timeZone = -9;
                break;

            case 6:
                //HAST
                //Hawaii does not use daylight savings
                timeZone = -10;
                daylightSavingsOn = false;
                break;
                
        }
        BlueSkiesManager.Instance()._timeZone = timeZone;
        BlueSkiesManager.Instance().TimeManager.setTime(hour, minute, seconds, timeZone, daylightSavingsOn);
    }

    public void updateTimeOfDaySlider()
    {
        TimeOfDaySlider.value = hour + minute / 60 + seconds / 3600;
        textTimeSliderValue.text = hour + ":" + minute + ":" + seconds;
    }

    public void UpdateAdvanceTimeRate()
    {   //Allows user to enter a rate that time passes in the scene
        if (ATRInput.text == "")
        {
            BlueSkiesManager.Instance()._advanceTime = false;
        }
        else
        {
            BlueSkiesManager.Instance()._advanceTime = true;
            //BlueSkiesManager.Instance().isUpdatingTime();
            BlueSkiesManager.Instance()._advanceTimeRate = float.Parse(ATRInput.text);
            BlueSkiesManager.Instance().updateTime();
            //BlueSkiesManager.Instance().TimeManager.getTime(out blueSkiesTime.getHour(), out blueSkiesTime.getMinute(), out blueSkiesTime.getSeconds());
        }
    }

    public void updateDaylightSavings()
    {

        if (month >= 3 && month < 11)
        {
            daylightSavingsOn = true;
            DaylightSavings.isOn = true;
        }
        else
        {
            daylightSavingsOn = false;
            DaylightSavings.isOn = false;
        }

        BlueSkiesManager.Instance()._daylightSavingsTime = daylightSavingsOn;
    }

    /* private void updateTime()
     {   //Updates the time
         if (advanceTimeRateBool == true)
         {
             float elapsed = Time.deltaTime * advanceTimeRate;
             UnityEngine.Debug.Log(elapsed);
             blueSkiesTime.addSeconds(elapsed);
             blueSkiesTime.getDate(out year, out month, out day);
             blueSkiesTime.getTime(out hour, out minute, out seconds);
         }

         BlueSkiesManager.Instance().SilverLining.update(blueSkiesTime, new Vector3((float)latitude, (float)longitude, (float)altitude));
     }*/

    public void updateLatLong()
    {

        if (LatitudeInput.text == "" || LongitudeInput.text == "" || AltitudeInput.text == "")
        {
            latitude = 39.4443f;
            longitude = -74.5633f;
            altitude = 75;
        }
        else
        {
            latitude = double.Parse(LatitudeInput.text);
            longitude = double.Parse(LongitudeInput.text);
            altitude = double.Parse(AltitudeInput.text);
        }
        BlueSkiesManager.Instance()._latitude = latitude;
        BlueSkiesManager.Instance()._longitude = longitude;
        BlueSkiesManager.Instance()._altitude = altitude;
        BlueSkiesManager.Instance().SilverLining.update(blueSkiesTime, new Vector3((float)latitude, (float)longitude, (float)altitude));
    }

    public string updateButtonText()
    {
        //sets ListBox layer button text
        if (precipName != " ")
        {
            textString += precipName + ", ";
        }
        if (cloudName != " ")
        {
            textString += cloudName + ", ";
        }
        if (windName != " ")
        {
            textString += windName + " at " + windSpeed + " mph";
        }

        return textString;
    }



    /// <summary>
    /// Create methods
    /// </summary>

    private void addCloud(CloudType type, Vector3 position, uint puffSize, Vector3 dimensions, bool isAlive = false, float lifetime = 0)
    {
        //adds single cloud
        ICloudDescriptor descriptor = new CloudDescriptor();
        descriptor.Type = (uint)type;
        descriptor.PuffSize = puffSize;
        descriptor.Origin = position;
        descriptor.Dimensions = dimensions;

        if (isAlive && lifetime != 0)
        {
            descriptor.IsAging = isAlive;
            descriptor.Lifetime = lifetime;
        }
        ulong cloudID = cloudManager.addCloud(descriptor);
        BlueSkiesManager.Instance().CloudManager.addCloud(descriptor);
        //CloudTypes.cs lists descriptor type values
        if (descriptor.Type == 6)
        {
            fogID = cloudID;
        }
        else
        {
            CloudIDList.Add(cloudID);
        }
        Debug.Log(cloudID);
    }

    public void addCloudLayer(CloudType type, Vector3 origin, Vector3 dimensions, bool stretchedToHorizon, float coverage, uint puffSize)
    {
        //adds cloud layer
        ICloudLayerDescriptor descriptor = new CloudLayerDescriptor();
        descriptor.Type = (uint)type;
        descriptor.PuffSize = puffSize;
        descriptor.Origin = origin;
        descriptor.Dimensions = dimensions;
        descriptor.Coverage = coverage;
        descriptor.StretchToHorizon = stretchedToHorizon;

        ulong cloudLayerID = cloudManager.addCloudLayer(descriptor);
        BlueSkiesManager.Instance().CloudManager.addCloudLayer(descriptor);
        CloudLayerIDList.Add(cloudLayerID);
        Debug.Log(cloudLayerID);
    }

    public void CreateWind()
    {
        //adds wind layer
        addWind(0, 1000, windSpeed, windDirection);
    }

    public void addWind(float minAltitude, float maxAltitude, float windSpeed, float direction)
    {
        //adds wind layer
        IWindVolume wind = new WindVolume();
        wind.MinAltitude = minAltitude;
        wind.MaxAltitude = maxAltitude;
        wind.WindSpeed = windSpeed;
        wind.WindDirection = direction;

        BlueSkiesManager.Instance().WindManager.addWind(wind);
        ulong windID = wind.UID;
        WindIDList.Add(windID);
        Debug.Log(windID);
        /*for (int i = 0; i < WindIDList.Count - 1; i++)
        {
            Debug.Log(WindIDList[i]);
        }*/
    }


    public void createTime(int time, float timeZone) //Not in use
    {
        BlueSkiesManager.Instance().TimeManager.setTime(time, 0, 0, timeZone, true);
    }

    public void createDate(int day, int month, int year) //Not in use
    {
        BlueSkiesManager.Instance().TimeManager.setDate(year, month, day);
        BlueSkiesManager.Instance().TimeManager.GetEpoch2000Centuries(true);

    }

    /// <summary>
    /// Delete methods
    /// </summary>
    /// 


    public void DeleteClouds()
    {
        //deletes all cloud layers
        foreach (Transform child in Cumulus.transform)
        {
            GameObject.Destroy(child.gameObject);
        }

        foreach (Transform child in Cirrus.transform)
        {
            GameObject.Destroy(child.gameObject);
        }
        Debug.Log("Clouds have been deleted");
    }

    public void destroyOneCloudLayer(ulong cloudLayerID)
    {
        //remove specified cloud layer
        BlueSkiesManager.Instance().CloudManager.removeCloudLayer(cloudLayerID);
    }

    public void destroyOneCloud(ulong cloudID)
    {
        //remove specified cloud layer
        BlueSkiesManager.Instance().CloudManager.removeCloud(cloudID);
    }

    public void DeleteWind()
    {
        //deletes all wind layers
        BlueSkiesManager.Instance().WindManager.clearWinds();
        Debug.Log("Wind has been deleted");
    }

    public void destroyOneWind(ulong windID)
    {
        //deletes specified wind
        BlueSkiesManager.Instance().WindManager.removeWind(windID);
        WindIDList.Remove(windID);
    }





    /// <summary>
    /// UI additions
    /// </summary>

    void addWeatherSystem()
    {
        updateButtonText();
        GameObject newScrollButton = (GameObject)Instantiate(buttonPrefab);
        newScrollButton.transform.SetParent(buttonPrefab.transform.parent, false);
        newScrollButton.GetComponentInChildren<Text>().text = textString;
        newScrollButton.SetActive(true);
        systemAspectList = new List<(string, ulong)>();

        if (PrecipitationDropDown.value != 0)
        {
            //GameObject precip = GameObject.Find(precipName);
            //precip.transform.parent = newScrollButton.transform;
            ulong addedPrecip = precipID;
            var tuple = ("precip", addedPrecip);
            systemAspectList.Add(tuple);
        }
        
        if (CloudCoverageDropDown.value != 0 && CloudCoverageDropDown.value % 2 != 0)
        {
            //GameObject clouds = GameObject.Find(cloudName);
            //clouds.transform.parent = newScrollButton.transform;

            ulong addedCloudLayer = CloudLayerIDList[CloudLayerIDList.Count - 1];
            var tuple = ("cloud layer", addedCloudLayer);
            systemAspectList.Add(tuple);

        }
        else if (CloudCoverageDropDown.value != 0 && CloudCoverageDropDown.value % 2 == 0)
        {
            ulong addedCloud = CloudIDList[CloudIDList.Count - 1];
            var tuple = ("cloud", addedCloud);
            systemAspectList.Add(tuple);
        }

        if (WindDirectionDropDown.value != 0 && WindSpeedInput.text != null)
        {
            ulong addedWind =  WindIDList[WindIDList.Count - 1];
            var tuple = ("wind", addedWind);
            systemAspectList.Add(tuple);
        }

        //Debug.Log(systemAspectList.Count);

        for (int i = 0; i <= systemAspectList.Count - 1; i++)
        {
            Debug.Log(systemAspectList[i]);
        }
        

    }

    public void deleteSystem()
    {
        for (int i = 0; i <= systemAspectList.Count - 1; i++)
        {
            if(systemAspectList[i].Item1 == "precip")
            {
                Rain.SetActive(false);
                Snow.SetActive(false);
                Sleet.SetActive(false);
            }

            else if (systemAspectList[i].Item1 == "cloud layer")
            {
                destroyOneCloudLayer(systemAspectList[i].Item2);
            }

            else if (systemAspectList[i].Item1 == "cloud")
            {
                destroyOneCloud(systemAspectList[i].Item2);
            }

            else if (systemAspectList[i].Item1 == "wind")
            {
                destroyOneWind(systemAspectList[i].Item2);
            }
        }
    }

    public void deleteListBoxButton(Button button)
    {
        
    }
}
