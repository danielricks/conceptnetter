import csv, re

'''
 Class Summary: ConceptNetter()
 Methods:	look_up_word([word])
			get_parts([word])
			get_related_words([word])
			get_hypernyms([word])
'''

class ConceptNetter:

	def __init__(self):
		self.load_conceptnet()

	# Creates a single file for all English information in Conceptnet 5. Takes about 1:41.
	def create_english_CSV_file(self):
		f = open("english_assertions.csv", "wb")
		output_file = csv.writer(f)
		for x in xrange(7):
			file_name = 'data/assertions/part_0' + str(x) + '.csv'
			print 'Loading ' + file_name
			with open(file_name, 'rb') as f:
				reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
				for row in reader:
					if '/c/en/' in row[0]:
						output_file.writerow(row)
		f.close()
		print 'Done creating ConceptNet 5 English file.'

	# Loads Conceptnet 5 into a dictionary. Takes about :54.
	def load_conceptnet(self):
		self.net = {}
		for x in xrange(1):
			file_name = "english_assertions.csv"
			print 'Loading ' + file_name
			with open(file_name, 'rb') as f:

				# Adds delimiting by tabs, otherwise the output looks a lot different
				reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
				for row in reader:

					# If the relationship is in the English language (deprecated)
					if '/c/en/' in row[0]:

						# Only use row[0] (the URI for a specific relationship)
						pieces = row[0].split(',')
						rel = pieces[0].split('/')[len(pieces[0].split('/')) - 2]
						surface_start = pieces[1].split('/')[len(pieces[1].split('/')) - 2].lower()
						surface_end = pieces[2].split('/')[len(pieces[2].split('/')) - 2].lower()

						# Verify that each word is longer than a single character, that Unicode characters don't show up in the output, and that other languages don't show up (Not sure if the '\\x' checks work)
						if len(surface_start) > 1 and not '\\x' in surface_start and len(surface_end) > 1 and not '\\x' in surface_end and rel != 'TranslationOf':

							# Checking whether a word had already been added was very inefficient, so now it's hacky
							try:
								self.net[surface_start].append(surface_start + ' ' + rel + ' ' + surface_end)
							except:
								self.net[surface_start] = []
								self.net[surface_start].append(surface_start + ' ' + rel + ' ' + surface_end)

							try:
								self.net[surface_end].append(surface_start + ' ' + rel + ' ' + surface_end)
							except:
								self.net[surface_end] = []
								self.net[surface_end].append(surface_start + ' ' + rel + ' ' + surface_end)
		print 'Done loading ConceptNet 5.'

	# Returns all information about a single word.
	def look_up_word(self, word):
		return self.net[word]

	# Returns all 'word HasA x' relationships in Conceptnet 5.
	def get_parts(self, word):
		rels = self.look_up_word(word)
		parts_rels = []
		for rel in rels:
			searchObj = re.search(word + ' HasA', rel, re.M|re.I)
			if searchObj:
				parts_rels.append(rel)
		return parts_rels

	# Returns all 'x RelatedTo word' relationships in Conceptnet 5.
	def get_related_words(self, word):
		rels = self.look_up_word(word)
		parts_rels = []
		for rel in rels:
			searchObj = re.search('RelatedTo ' + word, rel, re.M|re.I)
			if searchObj:
				parts_rels.append(rel)
		return parts_rels

	# Returns all 'word IsA x' relationships in Conceptnet 5.
	def get_hypernyms(self, word):
		rels = self.look_up_word(word)
		parts_rels = []
		for rel in rels:
			searchObj = re.search(word + ' IsA', rel, re.M|re.I)
			if searchObj:
				parts_rels.append(rel)
		return parts_rels

c = ConceptNetter()
c.create_english_CSV_file()

