# coding: utf-8
import cherrypy
from .database import Database_cl
from .view import View_cl

#----------------------------------------------------------
class Application_cl(object):
#----------------------------------------------------------

   #-------------------------------------------------------
   def __init__(self):
   #-------------------------------------------------------
      self.db_o = Database_cl()
      self.view_o = View_cl()

   @cherrypy.expose
   #-------------------------------------------------------
   def index(self, listform="startseite"):
   #-------------------------------------------------------
      #index Methode wird aufgerufen wenn root URL for the site is requested (http://localhost/)
      #so verändert, dass startseite als erste Seite angezeigt wird
      if listform == "listform=startseite":
         listform = "startseite"
      return self.createList_p(listform)

   @cherrypy.expose
   #-------------------------------------------------------
   def add(self, listform):
   #-------------------------------------------------------
      return self.createForm_p(listform)

   @cherrypy.expose
   #-------------------------------------------------------
   def edit(self, id_spl, listform):
   #-------------------------------------------------------
      return self.createForm_p(listform, id_spl)

   @cherrypy.expose
   #-------------------------------------------------------
   def save(self, id_spa, listform, name=None, vorname=None, akademischergrad=None, tätigkeit=None, bezeichnung=None, von=None, bis=None, beschreibung=None,max_teilnehmer=None,min_teilnehmer=None):
   #-------------------------------------------------------
   #Übergabeparameter für Eingabe
      id_s = id_spa
      if listform =="pflegemitarbeiterdaten":
         data_a = [name, vorname, akademischergrad, tätigkeit]
      elif listform =="pflegeweiterbildungen":
         data_a = [bezeichnung, von, bis, beschreibung,max_teilnehmer,min_teilnehmer]
      print("Es geht los")
      print(data_a)
      print("Es ist vorbei")
      if id_s != "None":
         self.db_o.update_px(id_s, data_a)
      else:
         self.db_o.create_px(data_a)
      return self.createList_p(listform)

   @cherrypy.expose
   #-------------------------------------------------------
   def delete(self, id, listform):
   #-------------------------------------------------------
      self.db_o.delete_px(id)
      raise cherrypy.HTTPRedirect('/' + "?listform=" + listform)
         

   @cherrypy.expose
   #-------------------------------------------------------
   def default(self, *arguments, **kwargs):
   #-------------------------------------------------------
      msg_s = "unbekannte Anforderung: " + \
      str(arguments) + \
      ' ' + \
      str(kwargs)
      raise cherrypy.HTTPError(404, msg_s)
   default.exposed= True

   #-------------------------------------------------------
   def createList_p(self, listform):
   #-------------------------------------------------------
      data_o = self.db_o.read_px()
      return self.view_o.createList_px(data_o, listform)

   #-------------------------------------------------------
   def createForm_p(self, listform ,id_spl = None):
   #-------------------------------------------------------
      if id_spl != None:
         data_o = self.db_o.read_px(id_spl)
      else:
         data_o = self.db_o.getDefault_px(listform)
      return self.view_o.createForm_px(listform, id_spl, data_o)
# EOF