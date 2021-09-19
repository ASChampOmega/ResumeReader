# Zip Folder Name -> Pdf Files -> List of Strings
# Read Files: From a list of given file names, takes each file name, opens it, and stores it as a list of strings

def get_zip(zip_name):
  with ZipFile(zip_name, 'r') as zip:
    print("Extracting Files Now")
    file_list = zip.namelist()
    zip.extractall()
    print(file_list)
  return file_list

def readPDFs(zip_name):
  file_list = get_zip(zip_name)
  file_list1 = []
  file_strings = []
  for file in file_list:
    file_1 = ""
    file_data = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(file_data)
    for page in range(0, pdfReader.numPages):
      page_obj = pdfReader.getPage(page)
      file_1 += " " + page_obj.extractText()
    file_strings.append(file_1)
    file_list1.append(file)
    file_data.close()
  return file_strings, file_list1

# Getting Input from the User

# If Skills are extracted, this asks the required skills
def ask_skills():
  print("You Indicated the skills you're looking for in candidates. Please enter all the skills you want the candidates to have")
  print("It is recommended that skills are entered as short verbs such as: lead for leadership, or manage for manager")
  print("This will increase matches and give a better output!")
  skills = input("Please enter the skills separated by single spaces \n")
  return format_skills(skills)

def format_skills(skills):
  L = []
  L = skills.split(' ')
  return L

def input_details():
  print("Please enter your requirements as a list of numbers")
  print("1 - Email Address (Recommended)")
  print("2 - Skills")
  print("3 - Projects")
  print("4 - Work and Education")
  print("5 - Scores")
  s1 = input("Input the above numbers (example: 1, 2, 5)  \n")
  L = []
  if('1' in s1):
    L.append(1)
  if('2' in s1):
    L.append(2)    
  if('3' in s1):
    L.append(3)
  if('4' in s1):
    L.append(4)
  if('5' in s1):
    L.append(5)
  if(2 in L):
    return L, ask_skills()
  return L, []

# Format the individual strings
def format_string(s):
  s1 = ""
  for c in s:
    if(c == '\n'):
      continue
    if(c == ":"):
      s1 += '\n'
      continue
    s1 += c
  s2 = ""
  prev = ""
  for c in s1:
    if(c == " " and prev == " "):
      s2 += "\n"
      prev = " "
    else:
      s2 += c
      prev = c
  return s2

# Extract Email Address

# Move backwards from an @ symbol
def move_back(s, i, last_char, last_idx):
  s1 = ""
  i -= 1
  while(i >= last_idx):
    if(s[i] in last_char):
      break;
    s1 += s[i]
    i -= 1
  return s1[::-1]

# Move forwards from an @ symbol
def move_front(s, i, last_char, last_idx):
  s1 = ""
  i += 1
  while(i < len(s) and i < last_idx):
    if(s[i] in last_char):
      break;
    s1 += s[i]
    i += 1
  return s1

# get the email address
def locate_address(s):
  addresses = []
  for i in range(len(s)):
    address = ""
    if(s[i] == '@'):
      address = move_back(s, i, [" "], 0) + "@" + move_front(s, i, [" "], len(s))
      addresses.append(address)
  return addresses

# Get a list of skills from a resume

def check_level_skill(s, i, window):
  sub = s.lower()
  sub = sub[i - window: i + window]
  count = 0
  j = i
  j -= 1
  for word in high_level_words:
    if(word in sub):
      return "(Advanced)"
  
  for word in intermediate_level_words:
    if(word in sub):
      return "(Intermediate)"
  for word in beginner_words:
    if(word in sub):
      return "(Beginner)"
  """
  j = i
  count = 0
  while(cout < window and j < len(split_text)):
    if(split_text[i] in high_level_words):
      return "(Advanced)"
    elif(split_text[i] in intermediate_level_words):
      return "(Intermediate)"
    elif(split_text[i] in beginner_words):
      return "(Beginner)"
    j += 1
    count += 1
  """
  return ""

def get_skills(s, skills_list, window):
  prev_pos_skill = {}
  curr_skills = []
  s1 = s.lower()
  for skill in skills_list:
    skill = skill.lower()
    prev_pos_skill[skill] = 0
  for skill in skills_list:
    curr_pos = s1.find(skill, prev_pos_skill[skill], len(s1))
    if(curr_pos != -1):
      level = check_level_skill(s1, curr_pos, window)
      curr_skills.append(skill + level)
      prev_pos_skill[skill] = curr_pos + len(skill)
  
  curr_skills = set(curr_skills)
  curr_skills = list(curr_skills)
  return curr_skills

nlp = spacy.load('en_core_web_sm')  

# Get the Projects:

def get_project_desc(s, i, end):
  curr = i
  s1 = s.lower()
  prev_pos_proj = {}
  list_projs = []
  for word in desc_words:
    prev_pos_proj[word] = 0
  for proj in desc_words:
    curr_pos = s1.find(proj, prev_pos_proj[proj], len(s1))
    if(curr_pos != -1 and curr_pos >= i and curr_pos < end + i):
      # print(curr_pos)
      back = move_back(s1, curr_pos, ['.', '\n', ';', ':'], i)
      front = move_front(s1, curr_pos, ['.', '\n',';', ':'], len(s))
      prev_pos_proj[proj] = curr_pos + len(proj)
      list_projs.append(back + proj[0] + front)
  
  list_projs = set(list_projs)
  list_projs = list(list_projs)
  return list_projs

def get_projects(s, width, skills_list, window):
  s1 = s.lower()
  all_projs = []
  for start in project_start:
    pos = s1.find(start)
    if(pos != -1):
      L1 = get_project_desc(s, pos, width)
    for proj in L1:
      all_projs.append(proj)
  all_projs = set(all_projs)
  all_projs = list(all_projs)
  all_projs_with_skills = {}
  for proj in all_projs:
    all_projs_with_skills[proj] = get_skills(proj, skills_list, window)

  return all_projs, all_projs_with_skills

more_common_words = ["gpa", "professional", "technical"]

# Get Background Experience

def get_work(s):
  doc = nlp(s)
  work = []
  for ent in doc.ents:
    if(ent.label_ == "ORG"):
      if(ent.text.lower() in desc_words or ent.text.lower() in skills_list or ent.text.lower() in more_common_words):
        continue
      work.append(ent.text)
  return work

# Scores
def get_scores(s):
  gpa_pos = s.find('GPA')
  scores = {}
  if(gpa_pos != -1):
    while(not s[gpa_pos].isnumeric()):
      gpa_pos += 1
    score_gpa = s[gpa_pos: gpa_pos + 4] + "/4.00"
    scores['gpa'] = score_gpa
  else:
    score_gpa = "Not_Found"
  return score_gpa

# Collect all the data in one place
def collect_data(s, L, skills_list, width, window):
  s1 = s.lower()
  all_data = {}
  flag = False
  if(1 in L):
    email_id = locate_address(s)
    if(email_id != ''):
      all_data["email_address"] = email_id
    else:
      all_data["email_address"] = "Not_Found"
      flag = True
  if(2 in L):
    skills_ind = get_skills(s, skills_list, window)
    if(skills_ind == []):
      all_data["skills"] = ["Not_Found"]
    else:
      all_data["skills"] = skills_ind
  if(3 in L):
    proj, proj_with_skills = get_projects(s, width, skills_list, window)
    if(proj == []):
      all_data["projects"] = {"None Found" : "NA"}
    else:
      all_data["projects"] = proj_with_skills
  if(4 in L):
    work = get_work(s)
    if(work == []):
      all_data["work"] = ["Not_Found"]
    else:
      all_data["work"] = work
  if(5 in L):
    gpa = get_scores(s)
    all_data['gpa'] = gpa
  return all_data

# Returns a string containing CSS for each page
def generate_header():
  head = """
  <!DOCTYPE html>
<html>
<head>
    <title> Trial 1</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <style>
        .email {
        }

        .projs {
        }

        .work {
        }

        .skills {
        }

        .gpa {
        }

        .skillsLi {
        }

        .projDesc {
        }
      </style>
  </head>
  <body>
  """
  return head

# Create the actual HTML layout

def make_html(L, all_data, filename):
  html = generate_header()
  if(1 in L):
    if(all_data['email_address'] != "Not_Found"):
      html += """
      <div class="email container p-3 my-3 bg-dark text-white">
        <h1> """ + filename + """ </h1>
        <h2> Email: """ 
      for email in all_data['email_address']:
        html += email + ", "
      html +=""" </h2>
      </div>
      """
    else:
      html += """ <div class="email container p-3 my-3 bg-dark text-white"> <h1> """ + filename + """ </h1> <h2> Email: Not Found </h2> </div> """
  if(2 in L):
    html += """
    <br> <div class="skills container">
      <h2> Skills </h2>
    """
    if(all_data['skills'] != ["Not_Found"]):
      html += """<ul class="list-group">"""
      for skill in all_data['skills']:
        html += """ <li class="list-group-item">""" + skill.capitalize() + """</li> """
      html += """ </ul> </div>"""
    else:
      html += """ <p> No Skills Found :( </p> </div>"""
  if(3 in L):
    html += """ <br> <div class="projs container">
        <h2> Projects </h2> """
    if(all_data['projects'] != {"None Found" : "NA"}):
      html += """ <ul class="list-group"> """
      count = 1
      for proj in all_data['projects']:
        html += """<li class="list-group-item">
                <div class="card">
                    <div class="card-body">
                        <h4 class="card-title">Project """ + str(count) + """ </h4>
                        <p class="card-text"> """ + proj.capitalize() + """ </p>
                        <ul class="list-group">
                        """
        for x in all_data['projects'][proj]:
          html += """ <li class="list-group-item"> """ + x.capitalize() + """ </li>"""
        html += """
                        </ul>
                    </div>
                </div>
            </li>"""
    else:
      html += "<p> No Projects found :( </p> </div>"
  
  if(4 in L):
    if(all_data['work'] != ["Not_Found"]):
      html += """ <br>
      <div class="work container">
        <h2> Background </h2>
        <ul class="list-group">
      """
      for exp in all_data["work"]:
        html += """ <li class="list-group-item"> """ + exp.capitalize() + """</li> """
      html += """ </ul> </div>"""
    else:
      html += "<p> No Background found :( </p> </div>"
  
  if(5 in L):
    html += """ <br>
        <div class="gpa container">
          <h1> GPA: """ + all_data['gpa'] + """ </h1>
      </div>
    """
  
  html += "</body> </html>"
  return html

def save_html(h, filename):
  with open(filename + '.html', 'w') as file:
    file.write(h)

# Get all .html files so that they can be zipped for the user

def get_all_file_paths(extension):
  file_paths = []
  entries = os.listdir()
  for entry in entries:
    if(entry[-5:-1] + entry[len(entry) - 1] == extension):
      file_paths.append(entry)
  return file_paths

# Zip the files

def zip_html(zip_name, file_names):
  with ZipFile(zip_name + '.zip','w') as zip:
    # writing each file one by one
    for file in file_names:
      zip.write(file)

# Bringing it all together

def extract_resume(zip_name):
  file_strings, file_list = readPDFs(zip_name)
  L, skills_list = input_details()
  print(skills_list)
  for i in range(len(file_strings)):
    file_strings[i] = format_string(file_strings[i])
    s = format_string(file_strings[i])
    all_data = collect_data(s, L, skills_list, 3000, 100)
    file_name = file_list[i][0:len(file_list[i]) - 4]
    html = make_html(L, all_data, file_name)
    save_html(html, file_name)
  zip_html('ExtractedResumes', file_names=get_all_file_paths('.html'))
  files.download("ExtractedResumes.zip")

