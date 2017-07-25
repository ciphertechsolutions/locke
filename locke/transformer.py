from abc import ABC, abstractmethod, abstractproperty
from multiprocessing import Process, Value, Array, Lock, Queue
import multiprocessing
import ctypes, math
import time, sys, os
import zipfile


class TransformString(ABC):
	"""
	Name: Transform String
	Description: Transform the whole data string
	ID: str_trans
	"""
	@abstractproperty
	def class_level():
		pass

	@abstractmethod
	def __init__(self, value):
		self.value = ""

	@abstractmethod
	def transform(self, data):
		"""
		Needs to be overridden
		This method contains all the requires steps/calls needed
		to transform the data string. After it finishes transforming
		the data, it needs to return a bytestring to be evaluated
	
		Args:
			data: The data that will be decoded by this method
	
		Returns:
			A bytestring
		"""
		if not isinstance(data, bytes):
			raise TypeError('Data (%s) needs to be a bytestring type' % type(data))
		return data

	@staticmethod
	@abstractmethod
	def all_iteration():
		"""
		Needs to be overridden
		This method will create a generator that lists/produces
		all the different iteration possible that this class
		can handle

		Return:
			A generator that produces all the different iteration
			that this class can use to transform the string. For
			example:

			If this class transform by XOR, this method will produce
			the value 1 - 256 (0 is the identity value for XOR).
		"""
		yield None


class TransformChar(ABC):
	"""
	Name: Transform Char
	Description: Transform individual char in the data (two bytes)
	ID: chr_trans
	"""
	@abstractproperty
	def class_level():
		pass

	@abstractmethod
	def __init__(self, value):
		self.value = value

	def transform(self, data):
		"""
		This method contains all the requires steps/calls needed
		to transform the string's individual char. This method
		should NOT be overridden.

		The way this method works is that it sends over all possible
		char values (0 - 256) to transform_char and then using string
		translation, it will modify the data as needed

		Args:
			data: The string that will be decoded by this method

		Returns:
			A bytestring
		"""
		if not isinstance(data, bytes):
			raise TypeError('Data (%s) needs to be a bytestring type' % type(data))
		trans_data = bytearray(data)
		for i in range(0, len(data)):
			trans_data[i] = self.transform_byte(data[i])
		return trans_data

	@abstractmethod
	def transform_byte(self, byte):
		"""
		This method will transform any char (or a byte from 0 - 256)
		and return the new char (with in the range 0 - 256).
		Args:
			byte: The numerical version of the char. This method should
			be able to handle all char from 0 - 256
		Returns:
			An int between 0 - 256
		"""
		pass

	@staticmethod
	@abstractmethod
	def all_iteration():
		"""
		Needs to be overridden
		This method will create a generator that lists/produces
		all the different iteration possible that this class
		can handle
		Return:
			A generator that produces all the different iteration
			that this class can use to transform the string. For
			example:

			If this class transform by XOR, this method will produce
			the value 1 - 256 (0 is the identity value for XOR).
		"""
		yield None


def rol_left(byte, count):
	"""
	This method will left shift the byte left by count
	Args:
		count: The numerical amount to shift by. Needs to be an int
		and greater or equal to 0
	Return:
		The byte shifted
	"""
	if (count < 0):
		raise ValueError('count needs to be larger than 0')
	if (not isinstance(count, int)):
		raise TypeError('count needs to be an int')

	count = count % 8
	# Shift left then OR with the part that was shift out of bound
	# afterward AND with 0xFF to get only a byte
	return (byte << count | byte >> (8 - count)) & 0xFF


def rol_right(byte, count):
	"""
	This method will right shift the byte left by count
	Args:
		count: The numerical amount to shift by. Needs to be an int
		and greater or equal to 0

	Return:
		The byte shifted
	"""
	if (count < 0):
		raise ValueError('count needs to be larger than 0')
	if (not isinstance(count, int)):
		raise TypeError('count needs to be an int')

	count = count % 8
	# Shift right then OR with the part that was shift out of bound
	# afterward AND with 0xFF to get only a byte
	return (byte >> count | byte << (8 - count)) & 0xFF


class Transfomer(object):

	def __init__(self, filename, password, transformers, patterns, zip,
			level, select, name_list, keep, save, verbose, process=4):

		process_pool = []
		self.verbose = verbose

		# Read the data
		global data 
		data = (self.read_file(filename) if not zip else
				self.read_zip(filename, password))

		transformer_list = self.select_transformers(transformers,
				name_list, select, level)

		# divide the transformer list
		group = math.ceil(len(transformer_list) / process)
		transformer_list = [transformer_list[i:i+group] 
				for i in range(0, len(transformer_list), group)]

		# create multiple process
		for i in range(0, len(transformer_list)):
			# TODO
			# Use QUEUE
			result = Queue()

			p = Process(target=self.evaluate_data, name="Eval %i" % i, 
					args=(transformer_list[i], keep, patterns, result))
			process_pool.append((p, result))
			p.start()

		for i in process_pool:
			i[0].join()

		results = []
		for i in process_pool:
			print("Getting data from %s" % i[0].name)
			results += i[1].get()

		self.write_file(filename, results, save)

	def read_zip(self, filename, password=None):
		"""
		Read a zip file and get the byte data from it. If there are multiple
		files inside the zip, it will ask which on to evaluate (or all if
		desired)
		Args:
			filename: The location of the file
			password: Defaults to None. The zip's password if applicable
		Return:
			Either a list of bytestring or a single bytestring
		"""
		if not zipfile.is_zipfile(filename):
			raise TypeError('\"%s\" is NOT a valid zip file! Try running a '
					'normal scan on it' % filename)

		zfile = zipfile.ZipFile(filename, 'r')

		print('What file do you want to evaluate:')
		for i in range(0, len(zfile.namelist())):
			print('%i: %s' % (i + 1, zfile.namelist()[i]))
		ans = int(input('1 - %i: ' % len(zfile.namelist())))

		if ans in range(1, len(zfile.namelist())):
			data = zfile.read(zfile.infolist()[ans - 1], password)
		else:
			raise IndexError('Range %i is out of bound' % ans)
		return data

	def read_file(self, filename):
		"""
		Read a file and return the bytestring
		Args:
			The location of the file
		Return:
			The bytestring of the file
		"""
		f = open(filename, 'rb')
		data = f.read()
		f.close()
		print("Done Reading %s" %filename)
		return data

	def select_transformers(self, trans_list, name_list, select, level):
		"""
		There is an order of precedent. If the names are provided, we will only
		use names, else the levels, else the only requested. Only one field
		will be used to find the list of transformers to be used
		Args:
			trans_list: A list of transformer to choose form
			name_list: A list of names to find
			level: The highest level allow for transformer
			only: The only level allowed to use
		Return:
			A list of transformer to use
		"""
		trans_class = []
		if name_list is not None:
			for name in name_list.split(','):
				for trans_level in trans_list:
					for trans in trans_level:
						if name.strip().lower() == trans[0].lower():
							trans_class.append(trans)
				if len(trans_class) == 0:
					sys.exit('No transformation found using \n%s' % name_list)
		elif select is not None:
			if select == 1:
				trans_class = trans_list[1]
			elif select == 2:
				trans_class = trans_list[2]
			elif select == 3:
				trans_class = trans_list[3]
			else:
				raise LookupError("There are no such level as %i" % select)
		else:
			if level == 1:
				trans_class = trans_list[0]
			elif level == 2:
				trans_class = trans_list[0] + trans_list[1]
			elif level == 3 or level is None:
				trans_class = trans_list[0] + trans_list[1] + trans_list[2]
			else:
				raise LookupError("There are no such level as %i" % level)
	
		if self.verbose:
			print("\t- Transformer to Use:")
			for trans in trans_class:
				print('\t\t- Class: %s | Level: %i' % (trans[0],
					trans[1].class_level()))
		return trans_class

	def evaluate_data(self, trans_list, keep, patterns, result):
		"""
		This method will transform the data it received and scan the data using
		its pattern database. Each pattern will have a weight that will help
		determine the score of each transformation on the data. The top highest
		score will be saved to disk. 
		Args:
			data: A bytestring to evaluate
			trans_list: The list of transformer to use
			keep: How many transformation to keep to stage 2
			patterns: The pattern class to use
			result: a c_char_p byte string to store the result
		Return:
			A list of tuples (transformer, score, data)
		"""
		name = multiprocessing.current_process().name
		print("%s Started" % name)

		results = []
		best_score = 0
	
		# Stage 1 pattern searching
		start_time = time.clock()
		for trans in trans_list:
			print("%s Working on Transformer: %s" % (name, trans[0]))
			for value in trans[1].all_iteration():
				# Create transformer and transform data
				transform = trans[1](value)
				trans_data = transform.transform(data)
				# Pattern search the transformed data
				score = 0
				for pat, matches in patterns.scan(trans_data):
					score += len(matches) * pat.weight
				#print('%s | Stage: 1 | Score: %i | Value: %s'
				#		% (trans[0], score, value), end='')
				#if score > best_score:
				#	best_score = score
				#	print('Best Score: %i | Stage: 1 | Transformer: %s' 
				#			% (best_score, trans[0]))
				results.append((transform, score))
		elapse = time.clock() - start_time
		print("%s ran through %i transforms in %f seconds - %f trans/sec"
				% (name, len(results), elapse, len(results)/elapse))
		# Sort the array and keep only the high scoring result
		results = sorted(results, key=lambda r: r[1], reverse=True)
		results = results[:keep]
		#for t, s in results:
		#	print("%s (%s) \t| Score: %s" % (t.__class__.__name__, t.value, s))
	
		print("%s Started on Stage 2" % name)
		#print("Stage 2 Scan")
		# Time for stage 2 pattern searching
		final_result = []
		start_time = time.clock()
		for i in range(0, len(results)):
			# Re transform the data
			transform, trans_score = results[i]
			print("%s Working on Transformer: %s" 
					% (name, transform.__class__.__name__))
			trans_data = transform.transform(data)
			# Search through the data with a more specific pattern
			score = 0
			for pat, matches in patterns.scan(trans_data):
				score += len(matches) * pat.weight
				#print("-- Pattern: %s | Matches: %i | Weight: %i"
				#		% (pat.name, len(matches), pat.weight))
			#print("Transform: %s | Score: %i"
			#		% (transform.__class__.__name__, score))

			#final_result.append((transform, score, trans_data))
			final_result.append((transform, score))
	
		elapse = time.clock() - start_time
		print("%s ran through %i transforms in %f seconds - %f trans/sec"
				% (name, i, elapse, i/elapse))
		# no returns as we are multiprocessing. result will be shared
		# to the parent process
		result.put(final_result)
		print("%s Finished" % name)

	def write_file(self, filename, results, save):
		# Write the final data to disk
		for transform, score in results[:save]:
			if score > 0:
				print("Tran: %s | Score %i" % (transform.__class__.__name__,
					score))
				base, ext = os.path.splitext(filename)
			t_filename = base + '_' + transform.__class__.__name__ + ext
			print("Saving to file %s" % t_filename)
			#open(t_filename, "wb").write(data)

# This was coded while listening to Nightcore
