! pip install -q PyPDF2
import PyPDF2
from zipfile import ZipFile
import spacy
import os
from google.colab import files
# Some Lists of key words
skills_list = ['c++', ' c ', 'machine learning', 'ml', 'nlp', 'natural language processing', 'python', 'java', '', '', '', '']
high_level_words = ['advanced', 'experienced', 'experience', 'good', 'proficient', 'efficient', 'difficult', 'challenging', 'tough',
                'hard', 'worked', 'projects', 'solid', 'excellent', 'analytical', 'quality', 'high',
                'skillful', 'skillfully', 'knowledge', 'knowledgeable', 'exceptionally', 'strong', 'mentored', 'interned', 'internship',
                'mentorship', 'award', 'extensive', 'significant', 'major', 'minor', 'certificate', 'certified', 'degree', 'bachelor', 
                'masters'
                ]

intermediate_level_words = ['intermediate', 'side']
beginner_words = ['beginner', 'bad', 'poor', 'new']
project_start = ["experience", "professional skill", "accomplishments", "achievements", "prizes", "awards", ]
desc_words = ["manage", "found", "discover", "won", "create", "develop", "compile", "design", "led", "innovate", "invent", "improve",
              "advise", "taught", "conduct", "spoke", "market", "establish", "promot", "maintain", "serve", "nominate", "implement",
              "train", 'certified', 'direct', 'guide', 'made', 'provide', 'schedule', 'convert', 'oversee', 'research', 'utilize',
              'recognize', 'eliminate', 'develop', 'simulate']
