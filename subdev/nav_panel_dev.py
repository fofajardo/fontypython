#!/usr/bin/python

import wx
from wx.lib.stattext import GenStaticText


class Link(GenStaticText):

    def __init__(self, *args, **kw):
        super(Link, self).__init__(*args, **kw)
        self.parent = args[0]
        self.font1 = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, True, 'Verdana')
        self.font2 = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD, False, 'Verdana')

        self.SetFont(self.font2)
        self.SetForegroundColour('#0000ff')

        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
        self.Bind(wx.EVT_MOTION, self.OnMouseEvent)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.parent.OnMouseEvent, self)

    def SetUrl(self, url):

        self.url = url


    def OnMouseEvent(self, e):

        if e.Moving():

            self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            self.SetFont(self.font1)

        elif e.LeftUp():

            print "goes to:", self.url
            wx.CallAfter(self.Foo, self)
            #self.parent.clickypoo(self)

        else:
            self.SetCursor(wx.NullCursor)
            self.SetFont(self.font2)
        print "e ends"
        e.Skip()

    def Foo(self,obj):
      print "call after for:", obj
      obj.Destroy()




class PagedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType,id)
        self.page = ""

myEVT_PAGED = wx.NewEventType()
EVT_PAGED = wx.PyEventBinder(myEVT_PAGED,1)


from wx.lib.stattext import GenStaticText

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
        
        self.hz = wx.BoxSizer(wx.HORIZONTAL)

        self.iid_prev = wx.NewId()
        self.iid_next = wx.NewId()
            

        self.SetSizer(self.hz)

        self.Bind(wx.EVT_SIZE, self.OnSize)    


    def DoGetBestSize(self):
        sz = self.parent.GetSize()
        self.CacheBestSize(sz)
        print sz
        return sz    

    def OnSize(self, evt):
        self.SetSize( self.parent.GetSize() )


    def set_list(self, itemlist):
        self._reset()

        self.fgz = wx.FlexGridSizer(cols = 1, vgap = 0, hgap = 4)
        
        self.gst_prev = GenStaticText(self,self.iid_prev,"<")
        self.gst_next = GenStaticText(self,self.iid_next,">")

        self.hz.Add(self.gst_prev)
        cols = len(itemlist)
        self.fgz.SetCols(cols)
        for i in itemlist:
            iid = wx.NewId()
            lbl = unicode(i)
            gst = GenStaticText(self, iid, lbl)
            d = {'iid':iid,'gst':gst}
            self._items.append(d)

            gst.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)
            #gst.Bind(wx.EVT_MOTION, self.OnMouseEvent)

            self.fgz.Add(gst,0,wx.EXPAND)
        self.hz.Add(self.fgz)
        self.hz.Add(self.gst_next)
        self.Layout()

    def _reset(self):
        self.hz.Clear(True) # clears fgz too
        #self.fgz.Clear(True)
        del self._items[:] #keeps list defined
        
    def goto_item(self,item):
        pass

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
            page = obj.GetLabel()
            iid = obj.GetId()
            #print "goes to:", page
            wx.CallAfter(self._page_clicked, page)
        else:
            self.SetCursor(wx.NullCursor)
        e.Skip()

    def _page_clicked(self, page):
        print "call after for:", page
        evt = PagedEvent(myEVT_PAGED, self.GetId()) 
        evt.page = page
        self.GetEventHandler().ProcessEvent(evt)



from random import random

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

        #CPU(self,-1)
        #cpu.addPages(10)
        self.SetSizer(vz)
        self.Layout()
        self.Centre()
        self.Show(True)

    def reset_links(self,evt):
        nl = range(0,int(random()*10)+1)
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
