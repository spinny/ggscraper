
import gtk

from all import ResultsCommon



class DomainsTab(ResultsCommon):

    COLUMN_NAME = "Domains"


    __domain__ = lambda self, l: l.split("//")[1].split("/")[0].lower()

    def __get_node__(self, link):
        dom = self.__domain__(link)
        if dom in self.__main_dict__:
            node = self.__main_dict__[dom]
        else:
            node = self.store.append(None, [dom])
            self.__main_dict__[dom] = node
        return node



