import netCDF4
import re
import datetime

class NCReader:

    def __init__(self, filename):
        self.lonName = ''
        self.latName = ''
        self.timeName = ''
        self.nc = netCDF4.Dataset(filename)

        for vn in self.nc.variables:
            v = self.nc.variables[vn]
            if hasattr(v, 'standard_name'):
                if v.standard_name.lower().strip() == 'longitude':
                    self.lonName = vn
                elif v.standard_name.lower().strip() == 'latitude':
                    self.latName = vn
                elif v.standard_name.lower().strip() == 'time':
                    self.timeName = vn

    def getLongitudes(self):
        return self.nc.variables[self.lonName][:]

    def getLatitudes(self):
        return self.nc.variables[self.latName][:]

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


    def getVariable(self, standard_name):
        var = []
        for vn in self.nc.variables:
            v = self.nc.variables[vn]
            if hasattr(v, 'standard_name') and v.standard_name == standard_name:
                return v[:]
        return var

###############################################################################

def test():
    n = NCReader('../data/tos_Omon_GFDL-CM4_historical_r1i1p1f1_gr_201001-201412.nc')
    lons = n.getLongitudes()
    print(f'longitudes: {lons}')
    lats = n.getLatitudes()
    print(f'latitudes: {lats}')
    dts = n.getDateTimes()
    print(f'times: {dts}')

if __name__ == '__main__':
    test()