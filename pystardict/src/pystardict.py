# -*- coding: utf-8 -*-

import gzip
import hashlib
import re
from struct import unpack

class _StarDictIfo(object):

    def __init__(self, dict_prefix, container):        
        ifo_filename = '%s.ifo' % dict_prefix
        try:
            _file = open(ifo_filename)
        except IOError:
            raise Exception('.ifo file does not exists')
        
        # skipping ifo header
        _file.readline()

        _line = _file.readline().split('=')
        if _line[0] == 'version':
            self.version = _line[1]
        else:
            raise Exception('ifo has invalid format')
        
        _config = {}
        for _line in _file:
            _line_splited = _line.split('=')
            _config[_line_splited[0]] = _line_splited[1]
        
        self.bookname = _config.get('bookname', None).strip()
        if self.bookname is None:
            raise Exception('ifo has no bookname')
        self.wordcount = _config.get('wordcount', None)
        if self.wordcount is None:
            raise Exception('ifo has no wordcount')
        self.wordcount = int(self.wordcount)
        
        if self.version == '3.0.0':
            try:
                _syn = open('%s.syn' % dict_prefix)
                self.synwordcount = _config.get('synwordcount', None)
                if self.synwordcount is None:
                    raise Exception('ifo has no synwordcount but .syn file exists')
                self.synwordcount = int(self.synwordcount)
            except IOError:
                pass
        
        self.idxfilesize = _config.get('idxfilesize', None)
        if self.idxfilesize is None:
            raise Exception('ifo has no idxfilesize')
        self.idxfilesize = int(self.idxfilesize)        
        self.idxoffsetbits = _config.get('idxoffsetbits', 32)
        self.idxoffsetbits = int(self.idxoffsetbits)
        self.author = _config.get('author', '').strip()
        self.email = _config.get('email', '').strip()
        self.website = _config.get('website', '').strip()
        self.description = _config.get('description', '').strip()
        self.date = _config.get('date', '').strip()
        self.sametypesequence = _config.get('sametypesequence', '').strip()


class _StarDictIdx(object):    
    def __init__(self, dict_prefix, container):
        
        idx_filename = '%s.idx' % dict_prefix
        idx_filename_gz = '%s.gz' % idx_filename
        
        try:
            file = open_file(idx_filename, idx_filename_gz)
        except:
            raise Exception('.idx file does not exists')
        
        """ check file size """
        self._file = file.read()
        if file.tell() != container.ifo.idxfilesize:
            raise Exception('size of the .idx file is incorrect')
        
        """ prepare main dict and parsing parameters """
        self._idx = {}
        idx_offset_bytes_size = int(container.ifo.idxoffsetbits / 8)
        idx_offset_format = {4: 'L', 8: 'Q',}[idx_offset_bytes_size]
        idx_cords_bytes_size = idx_offset_bytes_size + 4
        
        """ parse data via regex """
        record_pattern = r'([\d\D]+?\x00[\d\D]{%s})' % idx_cords_bytes_size
        matched_records = re.findall(record_pattern, self._file)
        
        """ check records count """
        if len(matched_records) != container.ifo.wordcount:
            raise Exception('words count is incorrect')
        
        """ unpack parsed records """
        for matched_record in matched_records:
            c = matched_record.find('\x00') + 1
            record_tuple = unpack('!%sc%sL' % (c, idx_offset_format),
                matched_record)
            word, cords = record_tuple[:c-1], record_tuple[c:]
            self._idx[word] = cords        
    
    def __getitem__(self, word):
        """
        returns tuple (word_data_offset, word_data_size,) for word in .dict
        
        @note: here may be placed flexible search realization
        """
        return self._idx[tuple(word)]
    
    def __contains__(self, k):
        """
        returns True if index has a word k, else False
        """
        return tuple(k) in self._idx
    
    def __eq__(self, y):
        """
        returns True if hashlib.md5(x.idx) is equal to hashlib.md5(y.idx), else False
        """
        return hashlib.md5(self._file).hexdigest() == hashlib.md5(y._file).hexdigest()
    
    def __ne__(self, y):
        """
        returns True if hashlib.md5(x.idx) is not equal to hashlib.md5(y.idx), else False
        """
        return not self.__eq__(y)

class _StarDictDict(object):
    
    def __init__(self, dict_prefix, container):
        self._container = container
        dict_filename = '%s.dict' % dict_prefix
        dict_filename_dz = '%s.dz' % dict_filename
        try:
            self._file = open_file(dict_filename, dict_filename_dz)
        except:
            raise Exception('.dict file does not exists')


    def __getitem__(self, word):
        cords = self._container.idx[word]
        self._file.seek(cords[0])
        bytes = self._file.read(cords[1])
        return bytes


class _StarDictSyn(object):
    
    def __init__(self, dict_prefix, container):
        syn_filename = '%s.syn' % dict_prefix
        try:
            self._file = open(syn_filename)
        except IOError:
            # syn file is optional, passing silently
            pass


class Dictionary(dict):

    
    def __init__(self, filename_prefix):

        self.ifo = _StarDictIfo(dict_prefix=filename_prefix, container=self)
        self.idx = _StarDictIdx(dict_prefix=filename_prefix, container=self)
        self.dict = _StarDictDict(dict_prefix=filename_prefix, container=self)
        self.syn = _StarDictSyn(dict_prefix=filename_prefix, container=self)

        self._dict_cache = {}
    
    def __cmp__(self, y):
        raise NotImplementedError()
    
    def __contains__(self, k):
        return k in self.idx
    
    def __delitem__(self, k):
        del self._dict_cache[k]
    
    def __eq__(self, y):
        return self.idx.__eq__(y.idx)
    
    def __ge__(self, y):
        raise NotImplementedError()
    
    def __getitem__(self, k):
        if k in self._dict_cache:
            return self._dict_cache[k]
        else:
            value = self.dict[k]
            self._dict_cache[k] = value
            return value
    
    def __gt__(self, y):
        raise NotImplementedError()
    
    def __iter__(self):
        raise NotImplementedError()
    
    def __le__(self):
        raise NotImplementedError()
    
    def __len__(self):
        return self.ifo.wordcount
    
    def __lt__(self):
        raise NotImplementedError()
    
    def __ne__(self, y):
        return not self.__eq__(y)
    
    def __repr__(self):
        return u'%s %s' % (self.__class__, self.ifo.bookname)
    
    def __setitem__(self, k, v):
        raise NotImplementedError()
    
    def clear(self):
        self._dict_cache = dict()
    
    def get(self, k, d=''):
        return k in self and self[k] or d
    
    def has_key(self, k):
        return k in self
    
    def items(self):
        raise NotImplementedError()
    
    def iteritems(self):
        raise NotImplementedError()
    
    def iterkeys(self):
        raise NotImplementedError()
    
    def itervalues(self):
        raise NotImplementedError()
    
    def keys(self):
        raise NotImplementedError()
    
    def pop(self, k, d):
        raise NotImplementedError()
    
    def popitem(self):
        raise NotImplementedError()
  
    def setdefault(self, k, d):
        raise NotImplementedError()
    
    def update(self, E, **F):
        raise NotImplementedError()
    
    def values(self):
        raise NotImplementedError()
    
    def fromkeys(self, S, v=None):
        raise NotImplementedError()


def open_file(regular, gz):
    try:
        return open(regular, 'rb')
    except IOError:
        try:
            return gzip.open(gz, 'rb')
        except IOError:
            raise ValueError('Neither regular nor gz file exists')
