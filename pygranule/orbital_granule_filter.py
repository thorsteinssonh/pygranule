

from .granule_filter import GranuleFilter
from .pyorbital_layer import PyOrbitalLayer

class OrbitalGranuleFilter(GranuleFilter):
    def __init__(self, input_config):
        GranuleFilter.__init__(self, input_config)
        # instanciate orbital layer
        aoi = self.get_aoi()
        sat = self._validated_config("sat_name")
        self.orbital_layer = PyOrbitalLayer(aoi,sat)

    def check_sampling_from_time(self, start, period=None):
        """
        Tests if granule at time step start samples (overlaps) target
        point / area of interest.
        """
        if period is None:
            period = self.get_time_step().total_seconds()/60.0
        
        return self.orbital_layer.does_swath_sample_aoi(start,period)

    def show(self, filepaths):
        """
        Shows an image for the area extent of the granules,
        and the target area.
        """
        dt = self.get_time_step()
        t = []
        for f in filepaths:
            t.append(self.source_file_name_parser.time_from_filename(f))
        
        self.orbital_layer.show_swath(t, period=dt.total_seconds()/60.0)
        
