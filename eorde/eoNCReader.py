import netCDF4
import datetime
import numpy

class NCReader(object):

    def __init__(self, filename):

        # we're after lat lon bounds (we cannot take the lats and lons as this would leave us with a gap)
        self.lonBoundsName = ''
        self.lonName = ''
        self.latBoundsName = ''
        self.latName = ''
        self.timeName = ''
        self.nc = netCDF4.Dataset(filename)

        for vn in self.nc.variables:
            v = self.nc.variables[vn]
            stdName = (getattr(v, 'standard_name', '') or getattr(v, 'long_name', '')).lower().strip()
            if stdName == 'longitude bounds':
                self.lonBoundsName = vn
            elif stdName == 'longitude':
                self.lonName = vn
            elif stdName == 'latitude bounds':
                self.latBoundsName = vn
            elif stdName == 'latitude':
                self.latName = vn
            elif stdName == 'time':
                self.timeName = vn

        # in some cases the bounds don't have a standard name and instead the 
        # coords had a bounds attribute that refers to the bounds
        if not self.lonBoundsName and self.lonName:
            v = self.nc.variables[self.lonName]
            self.lonBoundsName = getattr(v, 'bounds', '')
        if not self.latBoundsName and self.latName:
            v = self.nc.variables[self.latName]
            self.latBoundsName = getattr(v, 'bounds', '')


    def getLongitudes(self):
        if self.lonBoundsName:
            v = self.nc.variables[self.lonBoundsName]
            if len(v.shape) == 2:
                return self._getPointsFrom1DBounds(v)
            elif len(v.shape) == 3:
                return self._getPointsFrom2DBounds(v)
        # failure
        raise RuntimeError("ERROR: no longitudes!")


    def getLatitudes(self):
        if self.latBoundsName:
            v = self.nc.variables[self.latBoundsName]
            if len(v.shape) == 2:
                return self._getPointsFrom1DBounds(v)
            elif len(v.shape) == 3:
                return self._getPointsFrom2DBounds(v)
        # failure
        raise RuntimeError("ERROR: no latitudes!")


    def get2DLonsLats(self):
        lons = self.getLongitudes()
        lats = self.getLatitudes()
        if len(lons.shape) == 1:
            # 1d arrays
            lons, lats = numpy.meshgrid(lons, lats, indexing='xy')
        # already 2d arrays
        return lons, lats


    def getTimes(self):
        return self.nc.variables[self.timeName][:]


    def getTimeUnits(self):
        units = ''
        v = self.nc.variables[self.timeName]
        if hasattr(v, 'units'):
            units = v.units
        return units


    def getDateTimes(self):
        tv = self.getTimes()
        tu = self.getTimeUnits().split()
        dateStart = [int(i) for i in tu[2].split('-')] # year, month, day
        timeStart = [int(i) for i in tu[3].split(':')] # hour, minute, second
        dt0 = datetime.datetime(year=dateStart[0], month=dateStart[1], day=dateStart[2],
                                hour=timeStart[0], minute=timeStart[1], second=timeStart[2])
        deltas = tu[0]
        dts = [dt0 + eval('datetime.timedelta({}={})'.format(deltas, t)) for t in tv]
        return dts


    def getNetCDFVariableByStandardName(self, standard_name):
        res = None
        for vn in self.nc.variables:
            v = self.nc.variables[vn]
            stdName = getattr(v, 'standard_name', '') or getattr(v, 'long_name', '')
            if stdName == standard_name:
                return v
        raise RuntimeError(f"ERROR: no variable with standard_name or long_name {standard_name}")


    def getNetCDFVariableByName(self, name):
        return self.nc.variables[name]


    def _getPointsFrom1DBounds(self, v):
        x = numpy.zeros([v.shape[0] + 1], numpy.float64)
        x[:-1] = v[:, 0]
        x[-1] = v[-1, 1]
        return x


    def _getPointsFrom2DBounds(self, v):
        # add one to the number of cells
        shp = numpy.array(v[:, :, 0].shape) + numpy.array((1, 1))
        x = numpy.zeros(shp, numpy.float64)
        x[:-1, :-1] = v[:, :, 0]
        x[-1, :-1] = v[-1, :, 1]
        x[-1, -1] = v[-1, -1, 2]
        x[:-1, -1] = v[:, -1, 3]
        return x


###############################################################################

def test(filename):
    n = NCReader(filename)
    lons = n.getLongitudes()
    print(f'longitudes: {lons}')
    lats = n.getLatitudes()
    print(f'latitudes: {lats}')
    llons, llats = n.get2DLonsLats()
    dts = n.getDateTimes()
    print(f'times: {dts}')
    var = n.getNetCDFVariableByStandardName('sea_surface_temperature')
    print(f'var tos: {var}')

if __name__ == '__main__':
    test('data/sos_Omon_CESM2-WACCM_historical_r1i1p1f1_gn_185001-201412.nc')
    test('data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc')