import urllib2, smtplib

# Parameters for RestURL and Services to monitor
RestURL = "http://arcweb.ycpc.org/arcgis/rest" #Remove the 6080 door if necessary
services = ["Land_Base/Parcels","Parcels/Parcels"]

# Negative and Positive Parameters
RestURLNeg =""
RestURLPos =""

# Check if services are running and operational
count = 0
for s in services:
    url ="%s/services/%s/MapServer" %(RestURL,s)

    e = ""
    print(url)
    try:
        f = urllib2.urlopen(url, '5') # urllib2.urlopen(url[, data][, timeout in seconds])
        print f.code
        RestURLPos = RestURLPos + "\n"+ url + ": RESPONDING (code." + str(f.getcode()) + ")"
    except urllib2.HTTPError, e:
        print e.code
        RestURLNeg = RestURLNeg + "\n"+ url + ": NOT RESPONDING (code." + str(e.code) + ")"
    except urllib2.URLError, e:
        print e.args
        print e.reason.errno
        RestURLNeg = RestURLNeg + "\n"+ url + ": NOT RESPONDING (cod." + str(e.reason.errno) + ")"
    count = count+1

print(RestURLPos + "\n{} Service is operational".format(s.split("/")[1]))

if RestURLNeg != "" :
    import arcpy, sys, traceback, smtplib, datetime
    from email.mime.text import MIMEText
    print "{} \n{} Service is down".format(RestURLNeg, s.split("/")[1])
    # Run geoprocessing tool.
    # If there is an error with the tool, it will break and run the code within the except statement
    try:
        # Email when task completes
        # sender
        me = ""   # sending client email (the source email)
        # test recipient
        #you = "jsimora@ycpc.org"

        # recipient email
        you = "" # Add receipient email
        #you = 'jsimora@ycpc.org'

        # e-mail message container
        # e-mail message
        msg = MIMEText("To whom it may concern, \n \n\
        The following map service is down:\n{}".format(RestURLNeg[:-23]))

        # e-mail subject
        msg['Subject'] = "Map Service is Down"
        msg['From'] = me
        msg['To'] = you

        # server settings
        # Set name of email server and port number
        server = smtplib.SMTP_SSL('', 465) # email server example 'mail.sctfpa.org'

        server.set_debuglevel(1)
        #server.ehlo()
        #server.starttls()

        print "Created connection to e-mail server \n \n"

        # login to server
        server.login('', '') # First argument is the email server Username; Second argument is the email server password

        print"Logged in to e-mail server \n \n"

        # send message
        server.sendmail(me, [you], msg.as_string())

        print"Sent e-mail \n \n"

        # close server
        server.quit()

        print "Closed connection to server \n \n"

    # If an error occurs running geoprocessing tool(s) capture error and write message
    # handle error outside of Python system
    except EnvironmentError as ee:
        tbEE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        print "Failed at Line %i \n" % tbEE.tb_lineno
        # Write the error message to the log file
        print "Error: {}".format(str(ee))
    # handle exception error
    except Exception as e:
        # Store information about the error
        tbE = sys.exc_info()[2]
        # Write the line number the error occured to the log file
        print "Failed at Line %i \n" % tbE.tb_lineno
        # Write the error message to the log file
        print "Error: {}".format(e.message)
