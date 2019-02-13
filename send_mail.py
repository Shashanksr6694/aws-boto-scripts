import smtplib
import costReport
from costReport import getSummary
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

untagged_ec2=getSummary()['untagged_ec2']
untagged_ebs=getSummary()['untagged_ebs']

def send_email():
	try:
		email=' '                                        #write your email
		send_to_email=' '                                #write senders email  
		subject='Report Summary'
		message='Details about untagged EC2 instances and untagged EBS volumes'
		file_location1='/home/shashanksrivastava/Downloads/reports/untagged_instances.csv'
	        file_location1='/home/shashanksrivastava/Downloads/reports/untagged_volumes.csv'
		message_html="""
		<html>
			<body>
				<h1 style="color:rgb(51,51,51);font-weight:300;margin-top:20px;margin-bottom:10px">Digital AWS Accounts</h1>
				<hr style="border-style:solid none none;border-top-width:1px;border-top-color:rgb(221,221,221);margin-top:20px;					margin-bottom:20px;color:#5191d1;border:1px solid #5191d1;margin:0px 0px 20px 0px">
				<table style="font-family:&quot;Lucida Grande&quot;,Arial;font-size:18px;width:100%;border-spacing:0px">
		  			<tbody>
		  				<tr>
		      				<td><b>Account Name<b></td>
		      				<td style="text-align:left">
        		  				<b>Account Owner</b>
		      				</td>

 		     				<td style="text-align:left"><b>Cost($)</b></td>
   						</tr>
		    			<tr>
		      				<td>Oauth-AWS</td>
		      				<td style="text-align:left">
        		  				Shashank Srivastava
		      				</td>
 		     				<td style="text-align:left">{cost}</td>
   						</tr>
		        	</tbody>
	     		</table>
	     	</body>
	    </html>
		"""
		global untagged_ec2
		global untagged_ebs
		
		new_msg=message_html.format(cost=total_cost)
		msg=MIMEMultipart('alternative')
		msg['From']=email
		msg['To']=send_to_email
		msg['Subject']=subject
	
		msg.attach(MIMEText(message,'plain'))
		msg.attach(MIMEText(new_msg,'html'))

		filename1=os.path.basename(file_location1)
		filename2=os.path.basename(file_location2)
		filename3=os.path.basename(file_location3)
		filename4=os.path.basename(file_location4)
		file_list=[filename1,filename2,filename3,filename4]
		for f in file_list:
			attachment = open(f, "rb")
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % f)
			msg.attach(part)


		smtpObj=smtplib.SMTP('smtp.gmail.com',587)
		smtpObj.ehlo()	
		smtpObj.starttls()
		smtpObj.login(email,app_password)
		text=msg.as_string()
		smtpObj.sendmail(email,send_to_email,text)
		smtpObj.quit()
	except:
		print 'Something went wrong...'



send_email()
