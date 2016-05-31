import csv, re, os

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
		with open("conceptnetter/english_assertions.csv", "wb") as f:
			output_file = csv.writer(f)
			for x in xrange(7):
				file_name = 'conceptnetter/data/assertions/part_0' + str(x) + '.csv'
				print 'Loading ' + file_name
				with open(file_name, 'rb') as g:
					reader = csv.reader(g, delimiter='\t', quoting=csv.QUOTE_NONE)
					for row in reader:
						if '/c/en/' in row[0]:
							output_file.writerow(row)
		print 'Done creating ConceptNet 5 English file.'

	# Loads Conceptnet 5 into a dictionary. Takes about :54.
	def load_conceptnet(self):
		self.net = {}
		file_name = "conceptnetter/english_assertions.csv"
		if not os.path.exists(file_name):
			return
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

					# Check for Unicode characters.
					try:
						surface_start.decode('ascii')
						surface_end.decode('ascii')
					except:
						pass # It was a unicode format (Ex: '\xe9\x96\x80')
					else:

						# Verify that each word is longer than a single character and that other languages don't show up
						if len(surface_start) > 1 and len(surface_end) > 1 and rel != 'TranslationOf':

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
		pattern = word + ' HasA'
		return self.get_relationship(pattern, word)

	# Returns all 'x RelatedTo word' relationships in Conceptnet 5.
	def get_related_words(self, word):
		pattern = 'RelatedTo ' + word
		return self.get_relationship(pattern, word)

	# Returns all 'word IsA x' relationships in Conceptnet 5.
	def get_hypernyms(self, word):
		pattern = word + ' IsA'
		return self.get_relationship(pattern, word)

	# Returns a list of the words that match instances of a relationship.
	def get_relationship(self, pattern, word):
		pieces = pattern.split()
		result_index = 0
		# Decide whether the result word is in the 0th or the 2nd index
		if pieces[0] == word:
			result_index = 2
		# Get relationships for the word
		rels = self.look_up_word(word)
		parts_rels = []
		for rel in rels:
			searchObj = re.search(pattern, rel, re.M|re.I)
			# If the word exists...
			if searchObj:
				result = rel.split()[result_index]
				# If the relationship isn't backwords due to compound words ('trapdoor', etc.)...
				if result != word:
					parts_rels.append(result)
		return parts_rels

