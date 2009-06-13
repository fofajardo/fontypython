import wx

## Setup wxPython to access translations : enables the stock buttons.
langid = wx.LANGUAGE_DEFAULT # Picks this up from $LANG
mylocale = wx.Locale( langid )


from pubsub import *
from wxgui import ps

from gui_ScrolledFontView import *

import fpsys # Global objects
import fontyfilter


class SearchAssistant(wx.CollapsiblePane):
	def __init__(self, parent):
		self.label1=_("Click for Search Assistant")
		self.label2=_("Close Search Assistant")
		wx.CollapsiblePane.__init__(self,parent, label=self.label1,style=wx.CP_DEFAULT_STYLE)#|wx.CP_NO_TLW_RESIZE)
		self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPaneChanged)
		self.MakePaneContent(self.GetPane())
		
	def OnToggle(self, evt):
		self.Collapse(self.IsExpanded())
		self.OnPaneChanged()
		
	def OnPaneChanged(self, evt=None):
		#if evt:
		   # self.log.write('wx.EVT_COLLAPSIBLEPANE_CHANGED: %s' % evt.Collapsed)

		# redo the layout
		self.GetParent().Layout()

		# and also change the labels
		if self.IsExpanded():
			self.SetLabel(self.label2)
		else:
			self.SetLabel(self.label1)
		

	def MakePaneContent(self, pane):
		'''Just make a few controls to put on the collapsible pane'''
		nameLbl = wx.StaticText(pane, -1, _("Search Assistance.") )
		#name = wx.TextCtrl(pane, -1, "");
	#	city  = wx.TextCtrl(pane, -1, "", size=(150,-1));

		border = wx.BoxSizer()
		border.Add(nameLbl, 1, wx.EXPAND|wx.ALL, 5)
		pane.SetSizer(border)

class FontViewPanel(wx.Panel):
	"""
	Standalone visual control to select TTF fonts.
	The Panel that holds the ScrolledFontView control
	as well as the buttons etc. below and the text above.
	"""
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, id = -1)
		
		self.pageindex = 1 # I start here
		self.total_number_of_pages = 0
		
		self.filter = ""
		
		self.TICKMAP = None
		self.TICK = wx.Bitmap(fpsys.mythingsdir + "tick.png", type=wx.BITMAP_TYPE_PNG)
		self.CROSS = wx.Bitmap(fpsys.mythingsdir + "cross.png", type=wx.BITMAP_TYPE_PNG)
		
		## Main Label on top
		sizerMainLabel = wx.BoxSizer(wx.HORIZONTAL) 
		self.textMainInfo = wx.StaticText(self, -1, " ") 
		self.textMainInfo.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD))
		sizerMainLabel.Add(self.textMainInfo,1,wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT) 
		
		## Page choice and Filter controls
		sizerOtherControls = wx.BoxSizer(wx.HORIZONTAL)

		## The clear filter button: added 10 Jan 2008
		bmp = wx.Bitmap(fpsys.mythingsdir + "clear.png", type=wx.BITMAP_TYPE_PNG)
		self.clearButton = wx.BitmapButton(self, -1, bmp, style = wx.NO_BORDER)
		self.clearButton.SetToolTipString( _("Clear filter") )
		self.clearButton.Bind( wx.EVT_BUTTON, self.OnClearClick )
		
		## The filter text box
		self.textFilter = wx.StaticText(self, -1, _("Filter:"))
		#self.inputFilter = wx.TextCtrl(self, -1, "")
		#self.inputFilter.Bind(wx.EVT_CHAR, self.__evtChar) #catch the enter char

		self.inputFilter = wx.ComboBox(self, 500, "", (90, 50), 
						 (160, -1), [],
						 wx.CB_DROPDOWN
						 #| wx.TE_PROCESS_ENTER
						 #| wx.CB_SORT
						 )

		self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.inputFilter)
		self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, self.inputFilter)
		#self.inputFilter.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus) # Huh? Comes from the demo...
		#self.inputFilter.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


		self.last_filter_string = ""
		
		## The pager pulldown
		self.choicePage = wx.Choice(self, -1, choices = ["busy"]) 
		self.choicePage.Bind(wx.EVT_CHOICE, self.__onPagechoiceClick) #Bind choice event


		self.SA=SearchAssistant(self)

		## put them into the sizer
		sizerOtherControls.Add(self.textFilter, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
		sizerOtherControls.Add( self.clearButton, 0, wx.ALIGN_LEFT| wx.ALIGN_CENTER_VERTICAL ) # Clear button
		sizerOtherControls.Add(self.inputFilter, 1, wx.ALIGN_LEFT | wx.EXPAND)
		sizerOtherControls.Add(( 4,-1), 0, wx.EXPAND)
		sizerOtherControls.Add(( 4,-1), 0, wx.EXPAND)
		sizerOtherControls.Add(self.choicePage, 0 ,wx.EXPAND | wx.ALIGN_RIGHT)  #Added it to the sizer
		
		## The FONT panel:
		self.scrolledFontView = ScrolledFontView(self) 
		
		buttonsSizer = wx.BoxSizer(wx.HORIZONTAL) 
		self.buttPrev = wx.Button(self, wx.ID_BACKWARD) # Also not in Afrikaans.

		self.buttMain = wx.Button(self, label=" ", id = 3) 
		## This stock button has not been translated into Afrikaans yet. (Dec 2007)
		## I can't tell you how this fkuced me around!
		self.buttNext = wx.Button(self, wx.ID_FORWARD)  
		self.buttPrev.Enable(False)  #Starts out disabled
		
		buttonsSizer.Add(self.buttPrev,0,wx.EXPAND) 
		buttonsSizer.Add((10,1) ,0,wx.EXPAND) 
		buttonsSizer.Add(self.buttMain,1,wx.EXPAND) 
		buttonsSizer.Add((10,1) ,0,wx.EXPAND) 
		buttonsSizer.Add(self.buttNext,0,wx.EXPAND) 

		## Now the sizer to hold all the fontview controls
		self.sizerFontView = wx.BoxSizer( wx.VERTICAL )
		## The Main label
		self.sizerFontView.Add(sizerMainLabel, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 5 )
		## The font view
		self.sizerFontView.Add(self.scrolledFontView, 1, wx.EXPAND )

		## The Search Assistant
		self.sizerFontView.Add( self.SA, 0, wx.EXPAND)

		## Choice and Filter
		self.sizerFontView.Add(sizerOtherControls, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, border = 3)
		## The buttons   
		self.sizerFontView.Add(buttonsSizer,0,wx.EXPAND)	
		
		self.SetSizer(self.sizerFontView)
	
		e = wx.EVT_BUTTON #was wx.EVT_LEFT_UP
		self.buttPrev.Bind(e,self.__navClick) 
		self.buttNext.Bind(e,self.__navClick) 
		self.buttMain.Bind(e,self.__onMainClick) 
	
		ps.sub(toggle_main_button, self.ToggleMainButton) ##DND: class FontViewPanel
		ps.sub(update_font_view, self.MainFontViewUpdate) ##DND: class FontViewPanel
		ps.sub(reset_to_page_one, self.ResetToPageOne) ##DND: class FontViewPanel 

	def OnClearClick( self, event ):
		self.inputFilter.SetValue("") #was .Clear(), but that does not work for a combo box.
		self.filter = ""
		## Now command a change of the view.
		## First, return user to page 1:
		self.pageindex = 1
		self.__filterAndPageThenCallCreateFitmaps()
		self.buttMain.SetFocus()  #a GTK bug demands this move. Restore the ESC key func.

	# Capture events when the user types something into the control then
	# hits ENTER.
	def EvtTextEnter(self, evt):
		o=evt.GetEventObject()
		termsstring = evt.GetString()
		o.Append( termsstring )
		print "SEARCH FOR:", termsstring
		evt.Skip()

	# When the user selects something, we go here.
	def EvtComboBox(self, evt):
		cb = evt.GetEventObject()
		termsstring = evt.GetString()
		print termsstring

			
	## Catch the ENTER key in the filter text input control
	def __evtChar(self, e):
		if e.GetKeyCode() == 13:
			## Time to filter and redraw my list
			self.filter = self.inputFilter.GetValue()

			## First, return user to page 1:
			self.pageindex = 1

			## Now command a change of the view.
			self.__filterAndPageThenCallCreateFitmaps()

			self.buttMain.SetFocus()  #a GTK bug demands this move. Restore the ESC key func.
		if e.GetKeyCode() == 27:
			self.buttMain.SetFocus()
		e.Skip() #vital to keep the control alive!
		
	def __filterAndPageThenCallCreateFitmaps(self):
		"""
		Figure out what list of fonts to draw, divide them into pages,
		then go make Fitmaps out of them.
		"""
		
		self.total_number_of_pages = 1 # A default

		## Is there anything there to view?
		if len(fpsys.state.viewobject) > 0:

		## JUNE 2009 : Changes made

			## If the filter string changed from last time, signal so.
			filter_changed = False
			if self.filter != self.last_filter_string: filter_changed = True
			self.last_filter_string = self.filter

			## If the filter did change OR we have a blank filteredViewObject, then make a new one.
			if not fpsys.state.filteredViewObject or filter_changed:
				fpsys.state.filteredViewObject = fontyfilter.doFilter( self.filter ) # Uses the external module to filter.

			## STEP 2 : Figure out how many pages we have to display
			current_page = self.pageindex - 1
			num_in_one_page = fpsys.config.numinpage
			total_num_fonts = len(fpsys.state.filteredViewObject)

			# I miss the right words to explain this step, therefore an example:
			# 	23 / 10 = 2
			# 	23 % 10 = 3 > modulo > bool(3) = True = 1
			# 	-----------------------------------------
			# 	2 + 1 = 3 >  3 pages
			#
			#	40 / 10 = 4
			# 	40 % 10 = 0 > modulo > bool(0) = False = 0
			#	------------------------------------------
			# 	4 + 0 = 4 >	4 pages
			self.total_number_of_pages = (total_num_fonts / num_in_one_page) + bool(total_num_fonts % num_in_one_page)
			#print "total_num_fonts=", total_num_fonts
####		gross = total_num_fonts / float(num_in_one_page)
####		
####		if gross <= 1:
####			## There are less than num_in_one_page fonts to be viewed at all.
####			self.total_number_of_pages = 1
####		else:
####			## Okay, we have at least 1 page, perhaps more.
####			whole_number_of_pages = int(gross)
####			remainder = whole_number_of_pages % num_in_one_page
####			if remainder > 0: whole_number_of_pages += 1
####			self.total_number_of_pages = whole_number_of_pages

			start = current_page * num_in_one_page #leaf thru the pages to the one we are on now.
			fin = start + num_in_one_page
			if fin > len(fpsys.state.filteredViewObject): fin = len(fpsys.state.filteredViewObject) #Make sure we don't overshoot.
			
			## Extract a single page of fonts to display
			sublist = fpsys.state.filteredViewObject[start:fin] 
			
			## Empty the choice control.
			self.choicePage.Clear() 
			## Now refill it
			[self.choicePage.Append(str(n)) for n in xrange(1, self.total_number_of_pages +1)] 
			self.choicePage.SetSelection(self.pageindex-1)
		## The viewobject is empty anyway.
		else: 
			sublist = []

		if self.total_number_of_pages == 1: 
			self.choicePage.Enable(False) #I tried to hide/show the choice, but it would not redraw properly.
		else:
			self.choicePage.Enable(True)
			
		self.scrolledFontView.CreateFitmaps( sublist ) # Tell my child to draw the fonts
		self.__buttonState()


	def __onMainClick(self, e) :
		"""
		Removes fonts, or Appends fonts. Depends on situation in fpsys.state
		"""
		xPos, yPos = self.scrolledFontView.GetViewStart() #Saved by Robin Dunn, once again ! ! !
		wx.BeginBusyCursor()
		
		## Let's determine what kind of thing to do:
		if fpsys.state.action == "REMOVE":
			## We have a pog in viewobject and we must remove the selected fonts from it.
			vo = fpsys.state.viewobject
			victims = []
			dowrite = False
			for fi in vo:
				if fi.ticked:
					victims.append(fi) #Put it into another list
					dowrite = True
			for fi in victims:
				vo.remove(fi) #Now remove it from the vo
			del victims
			
			if dowrite:
				fpsys.flushTicks()
				bug = False
				try:
					vo.write()	  
				except(fontybugs.PogWriteError), e:
					bug = True
					self.errorBox([unicode( e ),])
				## Now, let's redraw the vo
				ps.pub( update_font_view )
				if not bug:
					ps.pub(print_to_status_bar,_("Selected fonts have been removed."))
				else:
					ps.pub(print_to_status_bar,_("There was an error writing the pog to disk. Nothing has been done"))
		
		## APPEND - Copy ttf to a pog.
		if fpsys.state.action == "APPEND":
			## We must append the fonts to the Pog
			vo = fpsys.state.viewobject
			to = fpsys.state.targetobject
			print _("Copying fonts from %(source)s to %(target)s") % {"source":vo.label(), "target":to.label()}
			dowrite = False
			for fi in vo:
				if fi.ticked:
					to.append(fi) 
					dowrite = True
			if dowrite: 
				fpsys.flushTicks() #Ensure we have no more ticks after a succ xfer.
				bug = False
				try:
					to.write()	  
				except(fontybugs.PogWriteError), e:
					bug = True
					self.ErrorBox( [repr( e )] )
				ps.pub( update_font_view )
				if not bug:
					ps.pub(print_to_status_bar,_("Selected fonts are now in %s.") % to.label())
				else:
					ps.pub(print_to_status_bar,_("There was an error writing the pog to disk. Nothing has been done"))
		
		## After pressing the button, the focus goes ... away ...
		## I don't know where and I'm trying to get it to go someplace
		## so that the ESC key continues working.
		## Forget it. I can't fix this. Onwards... other stuff to do!
		## self.menuBar.SetFocus()

		wx.EndBusyCursor()
		self.scrolledFontView.Scroll(xPos, yPos)

		
	def __onPagechoiceClick(self,event) :
		wx.BeginBusyCursor()
		if self.pageindex != int(event.GetString() ) : #Only redraw if actually onto another page.
			self.pageindex =  int(event.GetString() ) 
			self.__filterAndPageThenCallCreateFitmaps() 
		wx.EndBusyCursor()
		
	def __navClick(self,event) :
		wx.BeginBusyCursor()
		if event.GetId()  == wx.ID_FORWARD: 
			self.pageindex += 1
		else: #wx.ID_BACKWARD
			self.pageindex -= 1
		if self.pageindex > self.total_number_of_pages:
			self.pageindex = self.total_number_of_pages
		if self.pageindex == 0:
			self.pageindex = 1
		 
		self.buttMain.SetFocus()  #a GTK bug demands this move.
		self.__filterAndPageThenCallCreateFitmaps() 
		wx.EndBusyCursor()
		
	def __buttonState(self) :
		"""
		Enabled state of PREV/NEXT buttons
		"""
		n = True
		p = True
		if self.pageindex == self.total_number_of_pages: 
			n = False
		if self.pageindex == 1:
			p = False
		self.buttNext.Enable(n)		 
		self.buttPrev.Enable(p) 
		
	def ToggleMainButton(self):
		if fpsys.state.action == "NOTHING_TO_DO":
			self.buttMain.Enable( False )
			return
		if fpsys.state.numticks > 0: self.buttMain.Enable(True)
		else: self.buttMain.Enable(False)
			
	def MainFontViewUpdate(self):
		"""
		Vital routine - the heart if the app. 
		
		This decides what to do based on what has been selected.
		It draws the controls and the fonts as appropriate. 
		It also sets flags in fpsys.state
		"""
		
		## Get shorter vars to use.
		V = fpsys.state.viewobject
		T = fpsys.state.targetobject
			
		Vpatt = fpsys.state.viewpattern # View Pattern
		Tpatt = fpsys.state.targetpattern # Target pattern
	
		Patt = Vpatt + Tpatt # Patt = Pattern
		

		lab = ""
		status = ""
		
		## June 2009: A default value for this:
		self.TICKMAP = self.TICK

		## E == Empty View - no fonts in chosen Source.
		## N == Empty Target - no fonts.
		## P is Pog
		## F is Folder
		
		if Vpatt == "E": #NOTE : TESTING VPATT, not PATT - ergo: this covers E, EN, EP
			## Empty "E" - when the chosen Folder or Pog has NO FONTS IN IT.
			if Tpatt == "P":
				lab = _("Your active Target Pog is:%s") % T.name
				status = _("Please choose a Source.")
			else:
				lab = _("There are no fonts in here.")
				status = _("Please choose a Pog or a Font folder on the left.")
			btext = _("Nothing to do")
			fpsys.state.cantick = False
			fpsys.state.action = "NOTHING_TO_DO" # We will test this in mainframe::OnMainClick
			
		elif Patt == "FN":
			#View a Folder, no target
			lab = _("Viewing Folder:%s") % V.label()
			fpsys.state.cantick = False
			btext = _("Nothing to do")
			fpsys.state.action = "NOTHING_TO_DO" # We will test this in mainframe::OnMainClick
			status = _("Viewing a folder.")
		elif Patt == "PN": #A single Pog in the VIEW
			#View a pog, no target
			if V.isInstalled():
				## Cannot remove fonts from an installed pog
				lab = _("Viewing (installed) Pog: %s") % V.name
				btext = _("Nothing to do")
				fpsys.state.action = "NOTHING_TO_DO"
				fpsys.state.cantick = False
				status = _("You cannot change an installed Pog.")
			else:
				lab = _("Viewing (editable) Pog: %s") % V.name
				fpsys.state.cantick = True
				btext = _("Remove fonts from %s") % V.name
				self.TICKMAP = self.CROSS
				fpsys.state.action = "REMOVE" # We will test this in mainframe::OnMainClick
				status = _("You can remove fonts from the selected Target Pog.")
		elif Patt == "FP":
			#Folder to Pog
			if T.isInstalled():
				## We cannot put stuff into an installed pog
				lab = _("Viewing Folder:%s") % V.label()
				btext = _("Nothing to do")
				fpsys.state.action = "NOTHING_TO_DO"
				fpsys.state.cantick = False
				status = _("You cannot change an installed Pog.")
			else:
				lab = _("Append From: %(source)s To:%(target)s") % { "source":V.label(), "target":T.name }
				btext = _("Put fonts into %s") % T.name
				self.TICKMAP = self.TICK
				fpsys.state.cantick = True
				fpsys.state.action = "APPEND" # We will test this in mainframe::OnMainClick
				status = _("You can append fonts to your target Pog.")
		elif Patt == "PP":
			#Pog to Pog
			if T.isInstalled():
				## We cannot put fonts into an installed pog
				lab = _("Viewing Pog:%(source)s, but Pog:%(target)s is installed.") % {"source":V.name, "target":T.name}
				btext = _("Nothing to do")
				fpsys.state.action = "NOTHING_TO_DO"
				fpsys.state.cantick = False
				status = _("You cannot change an installed Pog.")
			else: #Not installed.
				if fpsys.state.samepogs: #Are the two pogs the same?
					## The validate routines determined the samepogs value.
					lab = _("These two are the same Pog.")
					fpsys.state.cantick = True
					btext = _("Nothing to do")
					fpsys.state.action = "NOTHING_TO_DO"
					status = _("Your Source and Target are the same Pog.")
				else: # Normal pog to pog
					lab = _("Append from Pog:%(source)s into Pog:%(target)s") % {"source":V.name, "target":T.name}
					btext = _("Put fonts into %s") % T.name
					self.TICKMAP = self.TICK
					fpsys.state.cantick = True	 
					fpsys.state.action = "APPEND" # We will test this in mainframe::OnMainClick
					status = _("You can append fonts to your target Pog.")
		else:
			print "MOJO ERROR: %s and trouble" % Patt
			raise SystemExit
			
		self.buttMain.SetLabel(btext)
		self.textMainInfo.SetLabel(lab)
		self.textMainInfo.Show()
		if status is not "":
			ps.pub(print_to_status_bar, status)
		self.ToggleMainButton()

		fpsys.markInactive()
		self.__filterAndPageThenCallCreateFitmaps()

	def ResetToPageOne(self):
		self.pageindex = 1 # I start here

