
from application import app
from flask import render_template,url_for, flash, get_flashed_messages,request,redirect
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from application.form import DateInputForm
from application.models import SelectionUserInput
import numpy as np



####REPLACE *** WITH YOUR CREDENTIALS, USERNAME, PASSWORDS, DATABASE NAMES, ETC

#ITEMS OF INTEREST:
item1='wallet'#***
item2='keys'#***



#####reference for azure SQL database communication: https://www.youtube.com/watch?v=JVtGKA6OVvM
import pypyodbc as odbc #pip install pypyodbc #for communication with azure database
from credential import username, password
server='***.database.windows.net' #address  of a Azure SQL server ("name" in Overview page)
database='***'
connection_string='Driver={ODBC Driver 18 for SQL Server};Server=tcp:'+server+',1433;Database='+database+';Uid='+username+';Pwd='+password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
conn = odbc.connect(connection_string)
table='***'

def fetchSQLtoDF (sqlquery): #function to make a query and convert and return the selected as pandas dataframe
    cursor=conn.cursor() #create instance of cursor object from connection object with reference to cursor method
    cursor.execute(sqlquery) #execute query with query method with sql statement
    dataset=cursor.fetchall() #fetch all that was queried into dataset
    columns =[column [0]  for column in cursor.description] #get column names from sql query object for database
    df=pd.DataFrame(dataset, columns=columns)
    df.loc[df.uidtag == '70 C3 D1 A0', 'rfidtype'] = item2 #assigning the item type ("RFIDtype") associated with uidtag to each such occurence
    df = df.sort_values(['date', 'time'],ascending = [False, False])#reordering entries by date and time for the latest to be on top
    df['date']= pd.to_datetime(df['date']).dt.date
    return df

df=fetchSQLtoDF('''SELECT * FROM dbo.'''+table)#extracting all entries from azure sql database table
latestDate=df['date'].max()  #last entry in dataframe
earliestDate=df['date'].min() #earliest entry in dataframe



@app.route('/', methods=['GET', 'POST']) 
def index():
    return render_template('index.html', title='index')

#ROUTE FOR BASE LAYOUT PAGE THAT GETS INHERITED BY OTHER PAGES, includes the dataset fetching from sql db
@app.route('/layout',methods=['GET', 'POST'])
def layout():
    global df
    df=fetchSQLtoDF('SELECT * FROM dbo.'+table)#extracting all entries from azure sql database table
    return render_template('layout.html')

#ROUTE FOR DATA TABLE #table creation based on https://www.youtube.com/watch?v=mCy52I4exTU
@app.route('/pdtable', methods=['GET', 'POST']) 
def pdtable():
    headings=df.columns.values.tolist()
    data=list(df.itertuples(index=False, name=None))
    return render_template('table.html',title='table', headings=df.columns.values.tolist(), data=list(df.itertuples(index=False, name=None)))

#ROUTE FOR DATE RANGE ADJUSTMENT
@app.route('/daterange', methods = ["POST", "GET"]) #daterange based on user start end date input
def daterange():
    global df
    df=fetchSQLtoDF('SELECT * FROM dbo.'+table)#extracting all entries from azure sql database table

    form = DateInputForm()
    if form.validate_on_submit():
        StartEndDate=SelectionUserInput(startdate=form.startdate.data, enddate=form.enddate.data)
        #startdate=pd.to_datetime(StartEndDate.startdate).date()
        #enddate=pd.to_datetime(StartEndDate.enddate).date()
        startdate=pd.to_datetime(StartEndDate.startdate).date()
        enddate=pd.to_datetime(StartEndDate.enddate).date()
        df = df[(df.date>startdate) & (df.date<enddate)]
        flash(f"The Overview Charts and Table have been adjusted to given range!")
        return render_template('daterange.html', title='daterange', form=form)
        #return redirect(url_for('overview'))
    return render_template('daterange.html', title='daterange', form=form, latestDate=latestDate, earliestDate=earliestDate)


############################################################################
###GRAPHS
#VARIABLES CONCERNING GRAPHS

#COLORS IN THE GRAPHS:
item1Clr='#ff9a1f'#'lightgrey'
item2Clr='#1f92b8'#'mediumturquoise'
lineWidth=1
ChartFont="Roboto"
fontSize=24

@app.route('/overview', methods=['GET', 'POST']) #ROUTE FOR CHARTS!
def overview():       
    global dfGroupedRfidType
    global dfGroupedDate
    dfGroupedRfidType=df.groupby('rfidtype').size().sort_values(ascending=False).reset_index(name='entries') #making small df with total counts of each RFID uidtag item entries
    dfGroupedDate=df.groupby(['date','rfidtype']).size().reset_index(name='entries')#making small df with total counts of each RFID uidtag item entries per day
    
    ###############
    #1 ############
    layout = go.Layout(plot_bgcolor='rgba(0,0,0,0)') #to make white background for all the bar charts etc
    # Create pie chart for total counts of each RFID uidtag item entries
    colors = [item1Clr, item2Clr, 'darkorange'] #defining used colors
    fig1 = go.Figure(data=[go.Pie(labels=dfGroupedRfidType.rfidtype,values=dfGroupedRfidType.entries, pull=[0.02,0])]) #making a piechart with pulled out sector
    fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=fontSize,marker=dict(colors=colors, line=dict(color='#000000', width=lineWidth)))#styling the pie chart, adding hover info 
    fig1.update_layout(title_text='Total Entries/RFID type',legend_title="", font=dict(family=ChartFont,size=fontSize,color="Black")) #adding the title, etc
    # Create graphJSON
    TotalTypepiegraphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    ###############
    #2 ############
    fig2 =  px.bar(dfGroupedDate, x='date', y='entries', color='rfidtype', barmode='group')
    fig2.update_xaxes(nticks=len(dfGroupedDate.date))
    fig2.update_xaxes(minor=dict(ticklen=6, tickcolor="black", showgrid=True))
    fig2.update_traces(overwrite=True, marker={"opacity": 1},marker_line_color='#000000', marker_line_width=lineWidth)
    fig2.update_layout(legend=dict(font=dict(size= fontSize)))
    fig2.for_each_trace(lambda trace: trace.update(marker_color=item1Clr) if trace.name == item1 else trace.update(marker_color=item2Clr) if trace.name == item2 else ())
    fig2.update_layout(title_text='Entries/Date/RFID type',legend_title="", font=dict(family=ChartFont,size=fontSize,color="Black")) #adding the title, etc
    fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})
    # Create graphJSON
    dateGraphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    ###############
    #3 ############
    df2 = df.filter(['rfidtype','date'], axis=1)
    df2['totalSec']=pd.to_timedelta(df.time).dt.total_seconds()
    df2['date'] = pd.to_datetime(df2['date'])
    df2['dayofWeek'] = df2['date'].dt.day_name()
    df2 = df2.sort_values(['dayofWeek', 'totalSec'],ascending = [False, False])


    x0 = df2[(df2['rfidtype'] == item2)].totalSec
    x1 = df2[(df2['rfidtype'] == item1)].totalSec

    fig3 = go.Figure(layout=layout)
    fig3.add_trace(go.Histogram(
        x=x0,
        histnorm='percent',
        name=item2, # name used in legend and hover labels
        xbins=dict(start=0,end=86400.0,size=3600),
        marker_color=item2Clr,
        opacity=1
    ))
    fig3.add_trace(go.Histogram(
        x=x1,
        histnorm='percent',
        name=item1,xbins=dict(start=0,end=86400,size=3600),
        marker_color=item1Clr,
        opacity=1
    ))

    fig3.update_layout(
        title_text='Peak Hours', # title of plot
        xaxis_title_text='Hour of the Day', # xaxis label
        yaxis_title_text='Entries', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )


    fig3.update_layout(xaxis = dict(tickvals=[(2*k-1)*3600/2 for k in range(1,25)],
            ticktext = list(range(0, 24+1))))
    fig3.update_xaxes(minor=dict(ticklen=6, tickcolor="black", showgrid=True))

    fig3.update_traces(overwrite=False, marker={"opacity": 1},marker_line_color='#000000', marker_line_width=lineWidth)
    fig3.for_each_trace(lambda trace: trace.update(marker_color=item1Clr) if trace.name == item1 else trace.update(marker_color=item2Clr) if trace.name == item2 else ())
    fig3.update_layout(title_text='Peak hours',legend_title="", font=dict(family=ChartFont,size=fontSize,color="Black")) #adding the title, etc

    # Create graphJSON
    dateGraphJSON2 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    ###############
    #4 ############
    fig4 = go.Figure(layout=layout)
    fig4.add_trace(go.Scatter(
    x=df2[(df2['rfidtype'] == item2)].dayofWeek,
    y=x0,
    marker=dict(color=item2Clr, size=fontSize,opacity=0.75),
    mode="markers",
    name=item2,))

    fig4.add_trace(go.Scatter(
    x=df2[(df2['rfidtype'] == item1)].dayofWeek,
    y=x1,
    marker=dict(color=item1Clr, size=fontSize,opacity=0.75),
    mode="markers",
    name=item1,
    ))

    fig4.update_layout(title="Hours of Entries per Days of the Week",
                  xaxis_title="Day of the Week",
                  yaxis_title='Hour of the Day')
    fig4.update_layout(yaxis = dict(tickvals=[(2*k-1)*3600/2 for k in range(1,25)],
            ticktext = list(range(0, 24+1))))
    fig4.update_traces(overwrite=False, marker={"opacity": 0.5},marker_line_color='#000000', marker_line_width=lineWidth)
    fig4.update_layout(legend_title="", font=dict(family=ChartFont,size=fontSize,color="Black")) #adding the title, etc
    fig4.update_layout(autosize=False,height=fontSize*30, width=fontSize*55)

    # Create graphJSON
    dateGraphJSON3 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
     
    #ALL THE GRAPHS PASSED TO OVERVIEW.HTML
    # Use render_template to pass graphJSON to html
    return render_template('overview.html', title='overview',totalPieGraphJSON=TotalTypepiegraphJSON, dateGraphJSON=dateGraphJSON, dateGraphJSON2=dateGraphJSON2, dateGraphJSON3=dateGraphJSON3)
