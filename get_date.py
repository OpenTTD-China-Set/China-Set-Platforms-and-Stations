# this program gets datetime
# and prints it to the console
import datetime

# get the current date and time in UTC
current_date = datetime.datetime.utcnow()

# convert current_date to string and append "UTC"
current_date_str = current_date.strftime("%Y-%m-%d %H:%M") + " UTC"

# read the file content
with open("custom_tags.txt", "r") as f:
    content = f.readlines()

# replace "%date" with current_date_str in the content
for index,item in enumerate(content):
    if "DATE" in item:
        content[index] = 'DATE    :' + current_date_str + "\n"

# write the new content back to the file
with open("custom_tags.txt", "w") as f:
    f.write("".join(content))
