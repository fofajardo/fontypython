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

        self._items = []
        self._current_page = self._last_page = 0

        self.hz = wx.BoxSizer(wx.HORIZONTAL)

        self.iid_prev = wx.NewId()
        self.iid_next = wx.NewId()
            

        self.SetSizer(self.hz)

        self.Bind(wx.EVT_SIZE, self.OnSize)    


    def DoGetBestSize(self):
        sz = self.parent.GetSize()
        #w=h=0
        #for itm in self._items:
        #    f = itm['gst'].GetFont()
        #    sz = f.GetPixelSize()
        #    w += sz[0]
        #    h += sz[1]
        self.CacheBestSize(sz)
        print sz
        return sz    

    def OnSize(self, evt):
        self.SetSize( self.parent.GetSize() )

    def _reset(self):
        self._current_page = self._last_page = 0
        self.hz.Clear(True) # clears fgz too
        #self.fgz.Clear(True)
        del self._items[:] #keeps list defined

    def _text(self,iid,lbl):
        f = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        f.SetPointSize(16)
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

    def set_list(self, itemlist):
        print "set_list:", itemlist
        self._reset()

        self.fgz = wx.FlexGridSizer(cols = 1, vgap = 0, hgap = 4)
        
        #self.gst_prev = GenStaticText(self,self.iid_prev,"<")
        self.gst_prev = self._text(self.iid_prev,"<")
        self.gst_next = self._text(self.iid_next,">")

        self.hz.Add(self.gst_prev)
        cols = len(itemlist)
        self.fgz.SetCols(cols)
        #self._items.append('dud')
        for i in itemlist:
            iid = wx.NewId()
            lbl = unicode(i)
            #gst = GenStaticText(self, iid, lbl)
            gst = self._text(-1, lbl)
            d = {'iid':iid,'gst':gst}
            self._items.append(d)

            gst.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
            #gst.Bind(wx.EVT_MOTION, self.OnMouseEvent)

            self.fgz.Add(gst,0,wx.EXPAND)
        self.hz.Add(self.fgz)
        self.hz.Add(self.gst_next)
        self.Layout()
        self.page_to(1)


    
    def _focus_off(self, item_index):
        gst = self._items[item_index-1]['gst']
        gst.SetBackgroundColour('yellow')
        self._unbold(gst)

    def _focus_on(self, item_index):
        gst = self._items[item_index-1]['gst']
        gst.SetBackgroundColour('red')
        self._enbold(gst)

    def page_to(self, item_index):
        self._focus_off(self._current_page)
        self._last_page = self._current_page
        self._current_page = item_index
        self._focus_on(item_index)


    def OnMouseEvent(self, e):
        """
<wx._core.MouseEvent; proxy of <Swig Object of type 'wxMouseEvent *' at 0x7ffd1d217d40> >
['AltDown', 'Aux1DClick', 'Aux1Down', 'Aux1IsDown', 'Aux1Up', 'Aux2DClick', 'Aux2Down', 'Aux2IsDown', 'Aux2Up', 'Button', 'ButtonDClick', 'ButtonDown', 'ButtonIsDown', 'ButtonUp', 'ClassName', 'Clone', 'CmdDown', 'ControlDown', 'Destroy', 'DidntHonourProcessOnlyIn', 'Dragging', 'Entering', 'EventObject', 'EventType', 'GetButton', 'GetClassName', 'GetClickCount', 'GetEventCategory', 'GetEventObject', 'GetEventType', 'GetId', 'GetLinesPerAction', 'GetLogicalPosition', 'GetModifiers', 'GetPosition', 'GetPositionTuple', 'GetSkipped', 'GetTimestamp', 'GetWheelAxis', 'GetWheelDelta', 'GetWheelRotation', 'GetX', 'GetY', 'HasModifiers', 'Id', 'IsButton', 'IsCommandEvent', 'IsPageScroll', 'IsSameAs', 'Leaving', 'LeftDClick', 'LeftDown', 'LeftIsDown', 'LeftUp', 'LinesPerAction', 'LogicalPosition', 'MetaDown', 'MiddleDClick', 'MiddleDown', 'MiddleIsDown', 'MiddleUp', 'Modifiers', 'Moving', 'Position', 'RawControlDown', 'ResumePropagation', 'RightDClick', 'RightDown', 'RightIsDown', 'RightUp', 'SetAltDown', 'SetAux1Down', 'SetAux2Down', 'SetControlDown', 'SetEventObject', 'SetEventType', 'SetId', 'SetLeftDown', 'SetMetaDown', 'SetMiddleDown', 'SetPosition', 'SetRawControlDown', 'SetRightDown', 'SetShiftDown', 'SetState', 'SetTimestamp', 'SetX', 'SetY', 'ShiftDown', 'ShouldProcessOnlyIn', 'ShouldPropagate', 'Skip', 'Skipped', 'StopPropagation', 'Timestamp', 'WasProcessed', 'WheelDelta', 'WheelRotation', 'X', 'Y', '__class__', '__del__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__swig_destroy__', '__weakref__', 'altDown', 'aux1IsDown', 'aux2IsDown', 'cmdDown', 'controlDown', 'leftIsDown', 'm_altDown', 'm_aux1Down', 'm_aux2Down', 'm_controlDown', 'm_leftDown', 'm_metaDown', 'm_middleDown', 'm_rightDown', 'm_shiftDown', 'm_x', 'm_y', 'metaDown', 'middleIsDown', 'rawControlDown', 'rightIsDown', 'shiftDown', 'this', 'thisown', 'x', 'y']
        """
        #print dir(e)
        #print e.GetEventObject().GetLabel()
        if e.Moving():
            #print "moving"
            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            #self.SetFont(self.font1)
        elif e.LeftUp():
            obj = e.GetEventObject()
            page_index = int(obj.GetLabel())
            iid = obj.GetId()
            #print "goes to:", page
            self.page_to( page_index )
            wx.CallAfter(self._page_clicked, page_index) # execs in the main thread after this event is done.
        else:
            self.SetCursor(wx.NullCursor)
        e.Skip()

    def _page_clicked(self, page_index):
        print "call after for:", page_index
        evt = PagedEvent(myEVT_PAGED, self.GetId()) 
        evt.page = page_index
        self.GetEventHandler().ProcessEvent(evt)




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

        self.np.set_list(range(1,20))

        self.SetSizer(vz)
        self.Layout()
        self.Centre()
        self.Show(True)

    def reset_links(self,evt):
        nl = range(1, int(random()*30)+1)
        nl=[1,]
        self.np.set_list(nl)
        print "reset done"

    def paged(self,evt):
        print "Got:", evt.page


def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
