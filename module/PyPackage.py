#!/usr/bin/env python
"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.

    @author: RaNaN
    @author: mkaay
"""

from module.PullEvents import UpdateEvent

class PyPackage():
    def __init__(self, manager, id, name, folder, site, password, queue, order, priority):
        self.m = manager
        self.m.packageCache[int(id)] = self

        self.id = int(id)
        self.name = name
        self.folder = folder
        self.site = site
        self.password = password
        self.queue = queue
        self.order = order
        self.priority = priority
        
        
        self.setFinished = False

    def toDict(self):
        """return data as dict

        format:

        {
            id: {'name': name ... 'links': {} } }
        }

        """
        return {
            self.id: {
                'id': self.id,
                'name': self.name,
                'folder': self.folder,
                'site': self.site,
                'password': self.password,
                'queue': self.queue,
                'order': self.order,
                'priority': self.priority,
                'links': {}
            }
        }

    def getChildren(self):
        """get information about contained links"""
        return self.m.getPackageData(self.id)["links"]
    
    def setPriority(self, priority):
        self.priority = priority
        self.sync()

    def sync(self):
        """sync with db"""
        self.m.updatePackage(self)

    def release(self):
        """sync and delete from cache"""
        self.sync()
        self.m.releasePackage(self.id)

    def delete(self):
        self.m.deletePackage(self.id)
                
    def notifyChange(self):
        e = UpdateEvent("pack", self.id, "collector" if not self.queue else "queue")
        self.m.core.pullManager.addEvent(e)