#!/usr/bin/python

import wx
from wx.lib.stattext import GenStaticText

from random import random

class PagedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType,id)
        self.page = 0

myEVT_PAGED = wx.NewEventType()
EVT_PAGED = wx.PyEventBinder(myEVT_PAGED,1)


class NavPanel(wx.PyPanel):
    def __init__(self, parent, id):
        self.parent = parent
        pos = wx.DefaultPosition
        sz = wx.Size( parent.GetSize()[0], -1)

        wx.PyPanel.__init__(self, parent, id,
                wx.DefaultPosition,
                sz,
                wx.NO_BORDER)
        self.SetBackgroundColour('yellow')
        #self.st = wx.StaticText(self, -1, "test", size = sz )

        self._items = {}
        self._current_page = self._last_page = 1



        
        f = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.ps = 14
        f.SetPointSize(self.ps)
        self.tile_size = f.GetPixelSize()

        self.hz = wx.BoxSizer(wx.HORIZONTAL)

        self.iid_prev = wx.NewId()
        self.iid_next = wx.NewId()

        self.gst_prev = self._text(self.iid_prev,"<")
        self.gst_next = self._text(self.iid_next,">")

        self.hz.Add(self.gst_prev)
        self.hz.AddSpacer(10)
        self.hz.Add(self.gst_next)            

        self.SetSizer(self.hz)
        self.Layout()


        self.Bind(wx.EVT_SIZE, self.OnSize)    
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def _chooser(self):
        ## The pager pulldown
        #pager_label = fpwx.label(self, _(u"Page:"))
        self.pager_combo = wx.ComboBox(self, -1,
                value="1", choices=["busy"],
                style = wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER )

        self.pager_combo.Bind(wx.EVT_COMBOBOX, self.onPagechoiceClick )
        self.pager_combo.Bind(wx.EVT_TEXT_ENTER, self.onPagerChoiceTextEnter )        

    def DoGetBestSize(self):
        #print "GBS"
        sz = self.parent.GetSize()
        #w=h=0
        #for itm in self._items:
        #    f = itm['gst'].GetFont()
        #    sz = f.GetPixelSize()
        #    w += sz[0]
        #    h += sz[1]
        self.CacheBestSize(sz)
        #print sz
        return sz    

    def OnSize(self, evt):
        self.SetSize( self.parent.GetSize() )

    #def _reset(self):
    #    self._current_page = self._last_page = 0
    #    self.hz.Clear(True)
    #    del self._items[:] #keeps list defined

    def _text(self,iid,lbl):
        f = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        f.SetPointSize(self.ps)
        f.SetWeight(wx.FONTWEIGHT_NORMAL)    

        gst = GenStaticText(self, iid ,lbl)
        
        gst.SetFont( f )
        return gst
    
    def _enbold(self,gst):
        f = gst.GetFont()
        f.SetWeight(wx.FONTWEIGHT_BOLD)
        gst.SetFont(f)

    def _unbold(self,gst):
        f = gst.GetFont()
        f.SetWeight(wx.FONTWEIGHT_NORMAL)
        gst.SetFont(f)

    def OnPaint(self,evt):
        # seems to happen on the various Set... calls
        pass

    def set_list(self, tot_num_pages, starting_page = 1):#numrange = None):
        self._current_page = self._last_page = starting_page

        self.hz.Remove(1)

        for pgnum, gst in self._items.iteritems():
            gst.Unbind(wx.EVT_MOUSE_EVENTS)
            gst.Destroy()
        self._items.clear()

        fgz = self.abbr_pages( tot_num_pages, starting_page)

        self.hz.Insert(1,fgz,0)

        self.Layout()
        #print "size of hz:", self.hz.GetSize()
        self.select_page_number( starting_page )



    def abbr_pages(self, n, page):
        """
        Return a string containing the list of numbers from 1 to `n`, with
        `page` indicated, and abbreviated with ellipses if too long.

        >>> abbreviated_pages(5, 3)
        '1 2 [3] 4 5'
        >>> abbreviated_pages(10, 10)
        '1 2 3 4 5 6 7 8 9 [10]'
        >>> abbreviated_pages(20, 1)
        '[1] 2 3 ... 18 19 20'
        >>> abbreviated_pages(80, 30)
        '1 2 3 ... 28 29 [30] 31 32 ... 78 79 80'



>>> import math
>>> d = int(math.log10(12))+1
>>> d
2
>>> l=[1,2,3,4,5,6,7,8,9,10,11]
>>> d = int(math.log10(11))+1
>>> d
2
>>> d = int(math.log10(10))+1
>>> d
2
>>> int(math.log10(9))+1
1
>>> [int(math.log10(n))+1 for n in l]
[1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2]
>>> sum([int(math.log10(n))+1 for n in l])
13
>>> 
        """
        assert(0 < n)
        assert(0 < page <= n)

        def build_pages_1(n,page):
            # Build set of pages to display
            if n <= 10:
                pages = set(range(1, n + 1))
            else:
                pages = (set(
                             range(1, 4)
                             )
                         | set( 
                             range( max(1, page - 2), min(page + 3, n + 1) )
                             )
                         | set(
                             range(n - 2, n + 1)
                             )
                         )
            return pages

        def build_pages_2(n, page):
            # Build set of pages to display
            foo = 10
            if n <= foo:
                pages = set(range(1, n + 1))
            else:
                foof = foo/3
                pages = (set(
                             range(1, foof)
                             )
                         | set( 
                             range( max(1, page - 2), min(page + foof, n + 1) )
                             )
                         | set(
                             range(n - foof, n + 1)
                             )
                         )
            return pages

        print "measure w:", self.GetSize()
        pages = build_pages_2( n, page)

        print pages

        # Display pages in order with ellipses
        def display():
            last_page = 0
            for p in sorted(pages):
                if p != last_page + 1: yield '...'
                #yield ('[{0}]' if p == page else '{0}').format(p)
                yield '{0}'.format(p)
                last_page = p
        
        pgs=[]
        for pg in display(): 
            pgs.append(pg)


        fgs = wx.FlexGridSizer(cols = 1, vgap = 0, hgap = 4)
        cols = len(pgs)
        fgs.SetCols(cols)

        for pg in pgs:
            lbl = unicode(pg)
            gst = self._text(-1,lbl)
            if lbl != "...":
                self._items.update({int(lbl):gst})
                gst.Bind(wx.EVT_MOUSE_EVENTS, self._pagelink_mouse_event)
            fgs.Add(gst,0,wx.EXPAND)
        return fgs
            
    def _focus_off(self, item_index):
        gst = self._items.get(item_index,None)
        gst.SetBackgroundColour('yellow')
        self._unbold(gst)

    def _focus_on(self, item_index):
        gst = self._items.get(item_index,None)
        gst.SetBackgroundColour('red')
        self._enbold(gst)

    def select_page_number(self, item_index):
        print self._current_page
        self._focus_off(self._current_page)
        self._last_page = self._current_page
        self._current_page = item_index
        self._focus_on(item_index)


    def _pagelink_mouse_event(self, e):

        #print dir(e)
        #print e.GetEventObject().GetLabel()
        if e.Moving():
            #print "moving"
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            #self.SetFont(self.font1)
        elif e.LeftUp():
            obj = e.GetEventObject()
            page_index = int(obj.GetLabel())
            #iid = obj.GetId()
            #print "goes to:", page
            self.select_page_number( page_index )
            wx.CallAfter(self._pagelink_clicked, page_index) # execs in the main thread after this event is done.
            #wx.CallAfter(self.set_list) # go back and re-draw myself.
        else:
            self.SetCursor(wx.NullCursor)
        e.Skip()

    def _pagelink_clicked(self, page_index):
        print "call after for:", page_index
        evt = PagedEvent(myEVT_PAGED, self.GetId()) 
        evt.page = page_index
        self.GetEventHandler().ProcessEvent(evt)

#for kid in self.fitmap_sizer.GetChildren():
#    fitmap = kid.GetWindow() #is the fitmap within


class Example(wx.Frame):

    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw)

        
        vz = wx.BoxSizer(wx.VERTICAL)

        pan_top = wx.Panel(self, wx.NewId())

        hbz = wx.BoxSizer(wx.HORIZONTAL)

        bid = wx.NewId()
        hb = wx.Button( pan_top, bid, 'reset')
        self.Bind(wx.EVT_BUTTON, self.reset_links,id = bid)

        hbz.Add(hb,0,wx.EXPAND)

        #bid = wx.NewId()
        #hb = wx.Button( pan_top, bid, 'add item')
        #self.Bind(wx.EVT_BUTTON, self.add_item,id = bid)
        
        #hbz.Add(hb,0,wx.EXPAND)
        pan_top.SetSizer(hbz)
        pan_top.Layout()

        vz.Add(pan_top, 0, wx.EXPAND)

        pan_bot = NavPanel(self, wx.NewId())
        self.Bind(EVT_PAGED, self.paged, pan_bot)

        self.np = pan_bot
        vz.Add(pan_bot,0,wx.EXPAND)

        self.np.set_list(20)#xrange(1,21))

        self.SetSizer(vz)
        self.Layout()
        self.Centre()
        self.Show(True)

    def reset_links(self,evt):
        nl = 500# range(1, 50)#int(random()*30)+1)
        #nl=[1,]
        self.np.set_list(nl, starting_page = 450)
        print "reset done"
        for kid in self.np.GetChildren():
            print kid
            #    fitmap = kid.GetWindow() #is the fitmap within

    def paged(self,evt):
        print "Got:", evt.page


def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()


rem = """<wx._core.MouseEvent; proxy of <Swig Object of type 'wxMouseEvent *' at 0x7ffd1d217d40> >
['AltDown', 'Aux1DClick', 'Aux1Down', 'Aux1IsDown', 'Aux1Up', 'Aux2DClick', 'Aux2Down', 'Aux2IsDown', 'Aux2Up', 'Button', 'ButtonDClick', 'ButtonDown', 'ButtonIsDown', 'ButtonUp', 'ClassName', 'Clone', 'CmdDown', 'ControlDown', 'Destroy', 'DidntHonourProcessOnlyIn', 'Dragging', 'Entering', 'EventObject', 'EventType', 'GetButton', 'GetClassName', 'GetClickCount', 'GetEventCategory', 'GetEventObject', 'GetEventType', 'GetId', 'GetLinesPerAction', 'GetLogicalPosition', 'GetModifiers', 'GetPosition', 'GetPositionTuple', 'GetSkipped', 'GetTimestamp', 'GetWheelAxis', 'GetWheelDelta', 'GetWheelRotation', 'GetX', 'GetY', 'HasModifiers', 'Id', 'IsButton', 'IsCommandEvent', 'IsPageScroll', 'IsSameAs', 'Leaving', 'LeftDClick', 'LeftDown', 'LeftIsDown', 'LeftUp', 'LinesPerAction', 'LogicalPosition', 'MetaDown', 'MiddleDClick', 'MiddleDown', 'MiddleIsDown', 'MiddleUp', 'Modifiers', 'Moving', 'Position', 'RawControlDown', 'ResumePropagation', 'RightDClick', 'RightDown', 'RightIsDown', 'RightUp', 'SetAltDown', 'SetAux1Down', 'SetAux2Down', 'SetControlDown', 'SetEventObject', 'SetEventType', 'SetId', 'SetLeftDown', 'SetMetaDown', 'SetMiddleDown', 'SetPosition', 'SetRawControlDown', 'SetRightDown', 'SetShiftDown', 'SetState', 'SetTimestamp', 'SetX', 'SetY', 'ShiftDown', 'ShouldProcessOnlyIn', 'ShouldPropagate', 'Skip', 'Skipped', 'StopPropagation', 'Timestamp', 'WasProcessed', 'WheelDelta', 'WheelRotation', 'X', 'Y', '__class__', '__del__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__swig_destroy__', '__weakref__', 'altDown', 'aux1IsDown', 'aux2IsDown', 'cmdDown', 'controlDown', 'leftIsDown', 'm_altDown', 'm_aux1Down', 'm_aux2Down', 'm_controlDown', 'm_leftDown', 'm_metaDown', 'm_middleDown', 'm_rightDown', 'm_shiftDown', 'm_x', 'm_y', 'metaDown', 'middleIsDown', 'rawControlDown', 'rightIsDown', 'shiftDown', 'this', 'thisown', 'x', 'y']
        """
