import netCDF4
import datetime
import numpy

class NCReader:

    def __init__(self, filename):
        self.EPS = 1.23e-10
        self.lonBoundsName = ''
        self.latBoundsName = ''
        self.timeName = ''
        self.nc = netCDF4.Dataset(filename)

        for vn in self.nc.variables:
            v = self.nc.variables[vn]
            longName = getattr(v, 'long_name', '').lower().strip()
            if longName == 'longitude bounds':
                self.lonBoundsName = vn
            elif longName.lower().strip() == 'latitude bounds':
                self.latBoundsName = vn
            elif longName == 'time':
                self.timeName = vn


    def getLongitudes(self):
        x = self.nc.variables[self.lonBoundsName][:, 0]
        x1 = self.nc.variables[self.lonBoundsName][-1, 1]
        return numpy.append(x, x1)


    def getLatitudes(self):
        y = self.nc.variables[self.latBoundsName][:, 0]
        y1 = self.nc.variables[self.latBoundsName][-1, 1]
        return numpy.append(y, y1)


    def get2DLonsLats(self):
        lons = self.getLongitudes()
        lats = self.getLatitudes()
        if len(lons.shape) == 1:
            lons, lats = numpy.meshgrid(lons, lats, indexing='xy')
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
            stdName = getattr(v, 'standard_name', '')
            lngName = getattr(v, 'long_name', '')
            if stdName == standard_name or lngName == standard_name:
                return v
        return res


    def getNetCDFVariableByName(self, name):
        return self.nc.variables[name]


###############################################################################

def test():
    n = NCReader('../data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc')
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
    test()