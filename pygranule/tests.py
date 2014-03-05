
import unittest

from .file_name_parser import FileNameParser
from .periodic_granule_filter import PeriodicGranuleFilter
from .orbital_granule_filter import OrbitalGranuleFilter
from .local_file_access_layer import LocalFileAccessLayer
from datetime import datetime

class TestLocalFileAccessLayer(unittest.TestCase):
    def setUp(self):
        self.fal = LocalFileAccessLayer()

    def test_list_directory(self):
        files = self.fal.list_directory("./")



class TestOrbitalGranuleFilter(unittest.TestCase):
    def setUp(self):
        config = {'config_name':"DummySatData",
                  'sat_name':"NOAA 19",
                  'file_source_pattern':"/home/msg/archive/AVHRR/avhrr_%Y%m%d_%H%M00_noaa19.hrp.bz2",
                  'time_step':"00:01:00",
                  'time_step_offset':"00:00:00",
                  'area_of_interest':"(-25,62.5),(-25,67),(-13,67),(-13,62.5)"}
        self.af = OrbitalGranuleFilter(config)
        # override orbital_layer with a particular TLE orbital element.
        self.af.orbital_layer.set_tle("1 29499U 06044A   11254.96536486  .00000092  00000-0  62081-4 0  5221",
                                      "2 29499  98.6804 312.6735 0001758 111.9178 248.2152 14.21501774254058")

    def test_validate(self):
        # Run
        result1 = self.af.validate("/home/msg/archive/AVHRR/avhrr_20140225_133400_noaa19.hrp.bz2")
        result2 = self.af.validate("/home/msg/archive/AVHRR/avhrr_20140225_133500_noaa19.hrp.bz2")
        result3 = self.af.validate("/home/msg/archive/AVHRR/avhrr_20140225_133600_noaa19.hrp.bz2")
        result4 = self.af.validate("/home/msg/archive/AVHRR/avhrr_20140225_133700_noaa19.hrp.bz2")
        result5 = self.af.validate("/home/msg/archive/AVHRR/avhrr_20140225_160000_noaa19.hrp.bz2")
        # Assert
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertFalse(result4)
        self.assertFalse(result5)

    def test_filter(self):
        # Run
        files = ["blabla",
                 "H-000-MSG3__-MSG3________-WV_073___-000009___-201401231300",
                 "/home/msg/archive/AVHRR/avhrr_20140225_133400_noaa19.hrp.bz2",
                 "/home/msg/archive/AVHRR/avhrr_20140225_133500_noaa19.hrp.bz2",
                 "/home/msg/archive/AVHRR/avhrr_20140225_133600_noaa19.hrp.bz2",
                 "/home/msg/archive/AVHRR/avhrr_20140225_133700_noaa19.hrp.bz2",
                 "/home/msg/archive/AVHRR/avhrr_20140225_160000_noaa19.hrp.bz2",
                 "H-000-MSG3__-MSG3________-IR_108___-000003___-201401231300"]
        result = self.af(files)
        # Assert
        self.assertItemsEqual(result,[files[2],files[3],files[4]])

class TestPeriodicGranuleFilter(unittest.TestCase):
    def setUp(self):
        config = {'config_name':"DummySatData",
                  'sat_name':"DummySat",
                  'file_source_pattern':"H-000-MSG3__-MSG3________-{0}___-00000{1}___-%Y%m%d%H%M",
                  'subsets':"{IR_108:{1..8}}",
                  'time_step':"00:15:00",
                  'time_step_offset':"00:00:00"}
        self.af = PeriodicGranuleFilter(config)

    def test_validate(self):
        # Run
        result1 = self.af.validate("blabla")
        result2 = self.af.validate("")
        result3 = self.af.validate("H-000-MSG3__-MSG3________-{0}___-00000{1}___-%Y%m%d%H%M")
        result4 = self.af.validate("H-000-MSG3__-MSG3________-IR_108___-000005___-%Y%m%d%H%M")
        result5 = self.af.validate("H-000-MSG3__-MSG3________-IR_108___-000005___-201402202301")
        # Assert
        self.assertFalse(result1)
        self.assertFalse(result2)
        self.assertFalse(result3)
        self.assertFalse(result4)
        self.assertFalse(result5)

    def test_filter(self):
        # Run
        files = ["blabla",
                 "H-000-MSG3__-MSG3________-IR_108___-000004___-201401231315",
                 "H-000-MSG3__-MSG3________-WV_073___-000002___-201401231355",
                 "H-000-MSG3__-MSG3________-WV_073___-000009___-201401231300",
                 "H-000-MSG3__-MSG3________-{0}___-00000{1}___-%Y%m%d%H%M",
                 "H-000-MSG3__-MSG3________-IR_108___-000003___-201401231300"]
        result = self.af(files)
        # Assert
        self.assertItemsEqual(result,[files[1],files[5]])

    def test_getitem(self):
        # Run
        value = self.af['time_step']
        # Assert
        self.assertEqual(value,"00:15:00")

class TestFileNameParser(unittest.TestCase):
    def setUp(self):
        self.fnp = FileNameParser("H-000-MSG3__-MSG3________-{0}___-00000{1}___-%Y%m%d%H%M",
                             "{IR_108:{1..8}, WV_073:{1,2,3,4,5,6,7,8}}")

    def test_filenames_from_time(self):
        reference_filenames = ['H-000-MSG3__-MSG3________-IR_108___-000001___-201401231355',
                               'H-000-MSG3__-MSG3________-IR_108___-000003___-201401231355',
                               'H-000-MSG3__-MSG3________-IR_108___-000002___-201401231355',
                               'H-000-MSG3__-MSG3________-IR_108___-000005___-201401231355',
                               'H-000-MSG3__-MSG3________-IR_108___-000004___-201401231355',
                               'H-000-MSG3__-MSG3________-IR_108___-000007___-201401231355',
                               'H-000-MSG3__-MSG3________-IR_108___-000006___-201401231355',
                               'H-000-MSG3__-MSG3________-IR_108___-000008___-201401231355',
                               'H-000-MSG3__-MSG3________-WV_073___-000001___-201401231355',
                               'H-000-MSG3__-MSG3________-WV_073___-000003___-201401231355',
                               'H-000-MSG3__-MSG3________-WV_073___-000002___-201401231355',
                               'H-000-MSG3__-MSG3________-WV_073___-000005___-201401231355',
                               'H-000-MSG3__-MSG3________-WV_073___-000004___-201401231355',
                               'H-000-MSG3__-MSG3________-WV_073___-000007___-201401231355',
                               'H-000-MSG3__-MSG3________-WV_073___-000006___-201401231355',
                               'H-000-MSG3__-MSG3________-WV_073___-000008___-201401231355']
        # Run
        t = datetime(2014,1,23,13,55)
        filenames = self.fnp.filenames_from_time(t)
        # Assert
        self.assertItemsEqual( filenames, reference_filenames )
    
    def test_time_from_filename(self):
        reference_t = datetime(2014,1,23,13,55)
        # Run
        t = self.fnp.time_from_filename("H-000-MSG3__-MSG3________-WV_073___-000006___-201401231355")
        # Assert
        self.assertEqual( t, reference_t )

    def test_validate_filename(self):
        # Run
        result1 = self.fnp.validate_filename("H-000-MSG3__-MSG3________-WV_073___-000006___-201401231355")
        result2 = self.fnp.validate_filename("H-000-MSG3__-MSG3________-WV_073___-00000X___-201401231355")
        # Assert
        self.assertTrue( result1 )
        self.assertFalse( result2 )


    def test_subset_from_filename(self):
        # Run
        subs1 = self.fnp.subset_from_filename('H-000-MSG3__-MSG3________-WV_073___-000003___-201401231355')
        # Assert
        self.assertItemsEqual(subs1,('WV_073', '3'))
        self.assertRaises(ValueError, self.fnp.subset_from_filename, ('H-000-MSG3__-MSG3________-Bla___-000003___-201401231355'))