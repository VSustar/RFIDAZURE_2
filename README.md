# RFIDAZURE_2
 <br><br>
## Home Project of RFID tracking, MS Azure SQL Database storage and WebApp Presentation
 <br> <br>
 The motive for the tracker is to keep track of items tagged with RFID tags. <br> <br>
            Project is compartmentalised into microcontroller (Esp32 in C) and cloud part (Azure IoTHub, SQL database and Python/HTML on Azure Webbapp). <br> <br>
            In this repository is the cloud part of the code in Python and HTML/CSS. 
 <br> <br>

            The sequence of whole process is as follows:

            1.RFID tagged items are registered by RFID reader and ESP32 microcontroller. 

            2.Each entry is sent to Azure cloud IoT hub by ESP32. </span>

            3.IoT hub events are directed into Azure SQL database via Streaming analytics job. 

            4.SQL database entries are queried by Python pypyodbc library. 

            5.The data is processed and presented via Python Pandas, Plotly and Flask libraries on webpage hosted by Azure Web App. 

            

 <br><br>
 <span align="middle"> <br>
 * This is the Web Page part of the code for RFID tracking to AZURE SQL DB and WebAPP data presentation with Python Pandas, Plotly and Flask</span>  
<span align="left"><img src="https://github.com/VSustar/RFIDAZURE_2/blob/main/images4github/RFIDdiagram3_Azure.png" width="100%"/></span>
<br><br>
<span align="middle"> <br>


## Page contains: 
<span align="middle"><br> 
 * Short intro</span>  
<span align="left"><img src="https://github.com/VSustar/RFIDAZURE_2/blob/main/images4github/Index.png" width="50%"/></span>
<span align="middle"><br> 
 * Charts made with Python libraries Pandas, Plotly and Flask with data queried from Azure SQL database where RFID data is stored.</span>  
<span align="left"><img src="https://github.com/VSustar/RFIDAZURE_2/blob/main/images4github/Overview.png" width="50%"/></span>
<span align="middle"><br> 
 * Table with data queried from Azure SQL database where RFID data is stored.</span>  
<span align="left"><img src="https://github.com/VSustar/RFIDAZURE_2/blob/main/images4github/table.png" width="50%"/></span>
<span align="middle"><br> 
 * Date range selector for the data from which the above charts and table are created. </span>  
<span align="left"><img src="https://github.com/VSustar/RFIDAZURE_2/blob/main/images4github/daterange.png" width="50%"/></span>

## Link to the RFID-ESP32 microcontroller part of the code
See [Github](https://github.com/VSustar/RFIDAZURE_1)
## Link to the Vid Sustar's RFID tracker WebPage
See [Wiki](https://github.com/luc-github/ESP3D/wiki/Install-Instructions)
