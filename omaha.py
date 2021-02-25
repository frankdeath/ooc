#!/usr/bin/env python
# file:         calc_gui.py
# usage:        calc_gui.py
# description:  GUI for the omaha calc script.
# author:       Kevin Peterson
# created:      June 13, 2004
# matured:      July 26, 2004

import wx
import wx.grid
import frame_icon
from random import randrange
from cards import *
from calc import *

ID_MENU_2=100
ID_MENU_3=101
ID_MENU_4=102
ID_MENU_5=103
ID_MENU_6=104
ID_MENU_7=105
ID_MENU_8=106
ID_MENU_9=107
ID_MENU_T=108
ID_MENU_J=109
ID_MENU_Q=110
ID_MENU_K=111
ID_MENU_A=112
ID_MENU_S=120
ID_MENU_H=121
ID_MENU_D=122
ID_MENU_C=123
ID_BUTTON1=125
ID_BUTTON2=126
ID_BUTTON3=127
ID_BUTTON4=128
ID_BUTTON5=129
ID_BUTTON6=140
ID_CARD_1=130
ID_CARD_2=131
ID_CARD_3=132
ID_CARD_4=133
ID_CARD_5=134
ID_CARD_6=135
ID_CARD_7=136
ID_CARD_8=137
ID_CARD_9=138
ID_EXIT=201
ID_ABOUT=202

FRAME_TITLE = "Omaha Odds Calculator"
FRAME_SIZE = (555,770)
COL_SIZE = 85
ROW_SIZE = 35

class CalcPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.hand_type = {0:'No Pair', 1:'One Pair', 2:'Two Pair', 3:'Three of a Kind', 4:'Straight', 5:'Flush', 6:'Full House', 7:'Four of a Kind', 8:'Straight Flush', 9:'Five of a Kind'}

        # Initialize the hand so that it's easier to implement active min hand calc
        #self.card_array = [12,11,51,50,10,9,8,7]
        self.card_array = [53] * 9

        self.right_clicked_card = -1
        self.right_click_selection = -1
        self.last_flop_array = [53] * 9
        self.last_turn_array = [53] * 9
        self.last_showdown_array = [53] * 9
        self.flop_turn_results = ()
        self.flop_river_results = ()
        self.flop_better_hands = []
        self.turn_river_results = ()
        self.turn_better_hands = []
        self.showdown_results = ()
        self.showdown_better_hands = []

        self.better = ()

        self.minipanel_is_open = 0
        self.minipanel = -1

        grid = wx.grid.Grid(self, -1, size = wx.Size(500, 347), style = wx.SIMPLE_BORDER)
        grid.CreateGrid(9, 5)
        grid.SetColLabelValue(0, "Hand")
        grid.SetColLabelValue(1, "Count")
        grid.SetColLabelValue(2, "Odds 1:x")
        grid.SetColLabelValue(3, "Probability")
        grid.SetColLabelValue(4, "# Better")
        grid.SetColSize(0, 160)
        grid.SetColSize(1, COL_SIZE)
        grid.SetColSize(2, COL_SIZE)
        grid.SetColSize(3, COL_SIZE)
        grid.SetColSize(4, COL_SIZE)
        grid.SetRowSize(0, ROW_SIZE)
        grid.SetRowSize(1, ROW_SIZE)
        grid.SetRowSize(2, ROW_SIZE)
        grid.SetRowSize(3, ROW_SIZE)
        grid.SetRowSize(4, ROW_SIZE)
        grid.SetRowSize(5, ROW_SIZE)
        grid.SetRowSize(6, ROW_SIZE)
        grid.SetRowSize(7, ROW_SIZE)
        grid.SetRowSize(8, ROW_SIZE)
        grid.SetColLabelSize(30)
        grid.SetRowLabelSize(0)
        grid.EnableEditing(False)
        grid.EnableDragColSize(False)
        grid.EnableDragRowSize(False)
        grid.EnableDragGridSize(False)
        grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        font = wx.Font(12, family = wx.ROMAN, style = wx.NORMAL, weight = wx.BOLD)
        grid.SetDefaultCellFont(font)
        # This is the magical line that turns off the scrollbars
        # Thank you: http://lists.wxwidgets.org/archive/wxPython-users/msg10178.html
        grid.SetMargins(-100,-100)

        self.grid = grid

        font = wx.Font(14, family = wx.MODERN, style = wx.NORMAL, weight = wx.BOLD)

        #self.title = wx.StaticText(self, -1, "", size=(250,25), style = wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE | wx.SIMPLE_BORDER, name = "Title")
        self.title = wx.StaticText(self, -1, "", size=(250,25), style = wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE, name = "Title")
        # font styles:
        # family = wx.DEFAULT, wx.DECORATIVE, wx.ROMAN, wx.SCRIPT, wx.SWISS, wx.MODERN
        # style = wx.NORMAL, wx.SLANT, wx.ITALIC
        # weight = wx.NORMAL, wx.LIGHT, wx.BOLD
        self.title.SetFont(font)

        title_sizer = wx.BoxSizer ( wx.HORIZONTAL )
        
        title_sizer.Add((30,30), 0, wx.ALIGN_CENTRE_VERTICAL)
        title_sizer.Add(self.title, 0, wx.ALIGN_CENTRE_VERTICAL)
        title_sizer.Add((30,30), 0, wx.ALIGN_CENTRE_VERTICAL)

        font = wx.Font(13, family = wx.MODERN, style = wx.NORMAL, weight = wx.BOLD)

        # call min_hand_eval here
        #current_h = self.MinHandEval()
        current_h = ""

        #self.hand_display = wx.StaticText(self, -1, current_h, size=(200,25), style = wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE | wx.SIMPLE_BORDER)
        self.hand_display = wx.StaticText(self, -1, current_h, size=(200,25), style = wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)
        self.hand_display.SetFont(font)

        # hutchison index
        #h_index = hutchison(self.card_array[:4])
        h_index = ""
        #self.hutch_display = wx.StaticText(self, -1, h_index, size=(200,25), style = wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE | wx.SIMPLE_BORDER)
        self.hutch_display = wx.StaticText(self, -1, h_index, size=(200,25), style = wx.ST_NO_AUTORESIZE | wx.ALIGN_CENTRE)
        self.hutch_display.SetFont(font)

        hand_disp_sizer = wx.BoxSizer( wx.HORIZONTAL )

        hand_disp_sizer.Add(self.hutch_display, 0 , wx.ALIGN_CENTER_VERTICAL)
        hand_disp_sizer.Add((30,50), 0, wx.ALIGN_CENTRE_VERTICAL)
        hand_disp_sizer.Add(self.hand_display, 0, wx.ALIGN_CENTRE_VERTICAL)
        #hand_disp_sizer.Add((30,50), 0, wx.ALIGN_CENTRE_VERTICAL)

        self.button1 = wx.Button(self, ID_BUTTON1, "Turn", size=(70,30))
        self.button2 = wx.Button(self, ID_BUTTON2, "River", size=(70,30))
        self.button3 = wx.Button(self, ID_BUTTON3, "River+", size=(70,30))
        self.button6 = wx.Button(self, ID_BUTTON6, "Showdown", size=(70,30))
        self.button4 = wx.Button(self, ID_BUTTON4, "Reset", size=(70,30))
        self.button5 = wx.Button(self, ID_BUTTON5, "Panel", size=(70,30))

        self.button1.Disable()
        self.button2.Disable()
        self.button3.Disable()
        self.button4.Disable()
        self.button6.Disable()

        button_sizer = wx.BoxSizer( wx.HORIZONTAL )

        LARGE_BUTTON_SPACE = (20, 40)
        MEDIUM_BUTTON_SPACE = (12, 40)
        SMALL_BUTTON_SPACE = (2, 40)

        button_sizer.Add(self.button5, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(LARGE_BUTTON_SPACE, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(self.button1, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(SMALL_BUTTON_SPACE, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(self.button2, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(MEDIUM_BUTTON_SPACE, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(self.button3, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(MEDIUM_BUTTON_SPACE, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(self.button6, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(LARGE_BUTTON_SPACE, 0, wx.ALIGN_CENTRE_VERTICAL)
        button_sizer.Add(self.button4, 0, wx.ALIGN_CENTRE_VERTICAL)

        # Initialize the cards
        self.card1 = wx.StaticBitmap(self, ID_CARD_1, catalog[index[self.card_array[0]]].getBitmap(), name = "Card1")
        self.card2 = wx.StaticBitmap(self, ID_CARD_2, catalog[index[self.card_array[1]]].getBitmap(), name = "Card2")
        self.card3 = wx.StaticBitmap(self, ID_CARD_3, catalog[index[self.card_array[2]]].getBitmap(), name = "Card3")
        self.card4 = wx.StaticBitmap(self, ID_CARD_4, catalog[index[self.card_array[3]]].getBitmap(), name = "Card4")
        self.card5 = wx.StaticBitmap(self, ID_CARD_5, catalog[index[self.card_array[4]]].getBitmap(), name = "Card5")
        self.card6 = wx.StaticBitmap(self, ID_CARD_6, catalog[index[self.card_array[5]]].getBitmap(), name = "Card6")
        self.card7 = wx.StaticBitmap(self, ID_CARD_7, catalog[index[self.card_array[6]]].getBitmap(), name = "Card7")
        self.card8 = wx.StaticBitmap(self, ID_CARD_8, catalog[index[self.card_array[7]]].getBitmap(), name = "Card8")
        self.card9 = wx.StaticBitmap(self, ID_CARD_9, catalog[index[self.card_array[8]]].getBitmap(), name = "Card9")

        self.cards = (self.card1, self.card2, self.card3, self.card4, self.card5, self.card6, self.card7, self.card8, self.card9)

        card_sizer1 = wx.BoxSizer( wx.HORIZONTAL )
        card_sizer2 = wx.BoxSizer( wx.HORIZONTAL )

        LITTLE_SPACER = (5,5)
        BIG_SPACER = (25,5)
        HOLE_SPACER = (5,125)

        card_sizer2.Add(self.card1, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer2.Add(HOLE_SPACER, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer2.Add(self.card2, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer2.Add(HOLE_SPACER, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer2.Add(self.card3, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer2.Add(HOLE_SPACER, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer2.Add(self.card4, 0, wx.ALIGN_CENTRE_VERTICAL)

        card_sizer1.Add(self.card5, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer1.Add(LITTLE_SPACER, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer1.Add(self.card6, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer1.Add(LITTLE_SPACER, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer1.Add(self.card7, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer1.Add(BIG_SPACER, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer1.Add(self.card8, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer1.Add(BIG_SPACER, 0, wx.ALIGN_CENTRE_VERTICAL)
        card_sizer1.Add(self.card9, 0, wx.ALIGN_CENTRE_VERTICAL)

        self.sizer = wx.BoxSizer( wx.VERTICAL )

        self.sizer.Add(title_sizer, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.Add(grid, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.Add(hand_disp_sizer, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.Add(card_sizer1, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.Add(card_sizer2, 0, wx.ALIGN_CENTRE_HORIZONTAL)

        self.sizer.Add(button_sizer, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)

        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick, self.grid)
        self.Bind(wx.EVT_BUTTON, self.OnButton5, self.button5)
        self.Bind(wx.EVT_BUTTON, self.OnButton1, self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButton2, self.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButton3, self.button3)
        self.Bind(wx.EVT_BUTTON, self.OnButton6, self.button6)
        self.Bind(wx.EVT_BUTTON, self.OnButton4, self.button4)
        self.card1.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card2.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card3.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card4.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card5.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card6.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card7.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card8.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card9.Bind(wx.EVT_LEFT_UP, self.LeftClick)
        self.card1.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.card2.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.card3.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.card4.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.card5.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.card6.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.card7.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.card8.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.card9.Bind(wx.EVT_RIGHT_UP, self.RightClick)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_2)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_3)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_4)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_5)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_6)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_7)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_8)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_9)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_T)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_J)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_Q)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_K)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_A)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_S)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_H)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_D)
        self.Bind(wx.EVT_MENU, self.OnMenuSelection, id=ID_MENU_C)

    def MinHandEval(self):
        if self.card_array[:7].count(53) == 0:
            combos = []
            combinations(self.card_array[:4], combos)
            min_hand = hand_evaluation(combos, self.card_array[4:7], self.card_array[7], self.card_array[8])
            return_value =  self.hand_type[min_hand]
        else:
            return_value = ""
        return return_value

    def LeftClick(self,e):
        self.left_clicked_card = e.GetId()
        card_index = self.left_clicked_card - 130
        random_card = randrange(52)
        found_random_card = False
        while found_random_card == False:
            # Check to see if the random card is already in the array of selected cards
            if self.card_array.count(random_card) == 0:
                self.card_array[card_index] = random_card
                self.cards[card_index].SetBitmap(catalog[index[random_card]].getBitmap())
                found_random_card = True
            else:
                random_card = randrange(52)

        # update the hand type label
        current_h = self.MinHandEval()
        self.hand_display.SetLabel(current_h)
        # update the hutchison index
        if card_index > -1 and card_index < 4: # also check to see if something actually changed
            #print "You changed a hole card"
            if self.card_array[:4].count(53) == 0:
                h_index = hutchison(self.card_array[:4])
                self.hutch_display.SetLabel(str(h_index))
        self.UpdateButtons()
        if self.minipanel_is_open == 1:
            self.minipanel.SyncWithMain()
        self.left_clicked_card = -1

    def RightClick(self,e):
        #print "mini panel is open = ", self.minipanel_is_open
        # record right-clicked card
        self.right_clicked_card = e.GetId()
        click_object = e.GetEventObject()
        # make a menu
        menu = wx.Menu()
        menu.Append(ID_MENU_A, "A")
        menu.Append(ID_MENU_K, "K")
        menu.Append(ID_MENU_Q, "Q")
        menu.Append(ID_MENU_J, "J")
        menu.Append(ID_MENU_T, "T")
        menu.Append(ID_MENU_9, "9")
        menu.Append(ID_MENU_8, "8")
        menu.Append(ID_MENU_7, "7")
        menu.Append(ID_MENU_6, "6")
        menu.Append(ID_MENU_5, "5")
        menu.Append(ID_MENU_4, "4")
        menu.Append(ID_MENU_3, "3")
        menu.Append(ID_MENU_2, "2")
        menu.AppendSeparator()
        menu.Append(ID_MENU_S, "Spades")
        menu.Append(ID_MENU_H, "Hearts")
        menu.Append(ID_MENU_D, "Diamonds")
        menu.Append(ID_MENU_C, "Clubs")

        # popup the menu. selected item's handler is called before popup menu returns
        click_object.PopupMenu(menu, e.GetPosition())
        menu.Destroy()
        # interpret what was selected, and then update the cards if necessary
        self.AfterMenuSelection()

        # update the hand type label
        current_h = self.MinHandEval()
        self.hand_display.SetLabel(current_h)
        # update the hutchison index
        if e.GetId() > 129 and e.GetId() < 134: # also check to see if something actually changed
            #print "You changed a hole card"
            if self.card_array[:4].count(53) == 0:
                h_index = hutchison(self.card_array[:4])
                self.hutch_display.SetLabel(str(h_index))
        self.UpdateButtons()
        if self.minipanel_is_open == 1:
            self.minipanel.SyncWithMain()

    def UpdateButtons(self):
        num_backs = self.card_array[:7].count(53)
        if num_backs == 7 and self.card_array[7] == 53 and self.card_array[8] == 53:
            self.button4.Disable()
        else:
            self.button4.Enable()
        if num_backs == 0:
            #print "Enable the flop calc buttons"
            self.button1.Enable()
            self.button2.Enable()
            if self.card_array[7] != 53:
                #print "Enable the turn calc button"
                self.button3.Enable()
                if self.card_array[8] != 53:
                    self.button6.Enable()
                else:
                    self.button6.Disable()
            else:
                self.button3.Disable()
                self.button6.Disable()
        else:
            self.button1.Disable()
            self.button2.Disable()
            self.button3.Disable()
            self.button6.Disable()

    def AfterMenuSelection(self):
        # interpret the selection
        if self.right_click_selection != -1:
            # get right clicked card
            card_index = self.right_clicked_card - 130
            # determine what was selected from the menu
            if self.right_click_selection < 115:
                # you selected a rank
                desired_rank = self.right_click_selection - 100
                ####print card_index
                if self.card_array[card_index] != 53:
                    # card has been defined, use existing suit.
                    desired_suit = self.card_array[card_index] / 13
                else:
                    # card has not been defined.  default suit = spades
                    desired_suit = 0
            else:
                # you selected a suit
                desired_suit = self.right_click_selection - 120
                if self.card_array[card_index] != 53:
                    # card has been defined, use existing rank.
                    desired_rank = self.card_array[card_index] % 13
                else:
                    # card has not been defined.  default card = Ace
                    desired_rank = 12
            # change the card to the desired one
            desired_card = desired_rank + desired_suit * 13
            # Check to see if card is already chosen.  If so, try to choose one of a different suit
            if self.card_array.count(desired_card) == 0:
                self.card_array[card_index] = desired_card
                self.cards[card_index].SetBitmap(catalog[index[desired_card]].getBitmap())
            else:
                #print "the card is already on the board--choosing one of another suit"
                other_suits = range(4)
                other_suits.remove(desired_suit)
                for i in other_suits:
                    temp_card = desired_rank + i * 13
                    if self.card_array.count(temp_card) == 0:
                        self.card_array[card_index] = temp_card
                        self.cards[card_index].SetBitmap(catalog[index[temp_card]].getBitmap())
                        break
        else:
            #print "you didn't select anything"
            dummy_variable = 1
        # reset the values to -1
        self.right_click_selection = -1
        self.right_clicked_card = -1

    def OnMenuSelection(self,e):
        self.right_click_selection = e.GetId()

    def UpdateGrid(self,flag):
        # 0 = flop_turn, 1 = flop_river, 2 = turn_river
        if flag == 0:
            data = self.flop_turn_results
            self.better = self.flop_better_hands
        elif flag == 1:
            data = self.flop_river_results
            self.better = self.flop_better_hands
        elif flag == 2:
            data = self.turn_river_results
            self.better = self.turn_better_hands
        elif flag == 3:
            data = self.showdown_results
            self.better = self.showdown_better_hands
        else:
            print "Major Error!"

        # data: (counter, type_counter[], odds[], prob[]))
        self.grid.BeginBatch()
        # update label for total number enumerated
        self.grid.SetColLabelValue(1, "Out of %d" % data[0])
        # update rows of data
        for i in range(9):
            # update hand types
            self.grid.SetCellValue(8-i,0,self.hand_type[i])
            # update count
            self.grid.SetCellValue(8-i,1,str(data[1][i]))
            # update odds
            if data[2][i] == 0.0:
                disp_string = "---"
            else:
                disp_string = "%.2f" % data[2][i]
            self.grid.SetCellValue(8-i,2,disp_string)
            # update prob
            disp_string = "%.2f" % data[3][i]
            self.grid.SetCellValue(8-i,3,disp_string)
            # update better hands
            self.grid.SetCellValue(8-i,4,str(self.better[0][i]))
        self.grid.EndBatch()

    def CalcIfNecessary(self,flag):
        #print "self.card_array", self.card_array
        #print "sefl.last_flop_array", self.last_flop_array
        #print "sefl.last_turn_array", self.last_turn_array

        # 0 = flop_turn, 1 = flop_river, 2 = turn_river
        if flag < 2:
            # do flop calc
            if self.card_array[:7] != self.last_flop_array[:7]:
                #print "I'm doing a calculation"
                self.flop_turn_results, self.flop_river_results, self.flop_better_hands = calculate_flop(self.card_array[:4], self.card_array[4:7])
                self.last_flop_array = self.card_array[:]
        elif flag == 2:
            # do turn calc
            if self.card_array[:8] != self.last_turn_array[:8]:
                #print "I'm doing a calculation"
                self.turn_river_results, self.turn_better_hands = calculate_turn(self.card_array[:4], self.card_array[4:8])
                self.last_turn_array = self.card_array[:]
        else:
            # do showdown calc
            if self.card_array != self.last_showdown_array:
                #print "I'm doing a calculation"
                self.showdown_results, self.showdown_better_hands = calculate_river(self.card_array[:4], self.card_array[4:])
                self.last_showdown_array = self.card_array[:]
                
        self.UpdateGrid(flag)

    def OnButton1(self,e):
        # check to make sure calculation can be done
        #if self.card_array[:7].count(53) == 0:
        self.title.SetLabel("Turn")
        self.CalcIfNecessary(0)

    def OnButton2(self,e):
        # check to make sure calculation can be done
        #if self.card_array[:7].count(53) == 0:
        self.title.SetLabel("River w/o turn card")
        self.CalcIfNecessary(1)

    def OnButton3(self,e):
        # check to make sure calculation can be done
        #if self.card_array.count(53) == 0:
        self.title.SetLabel("River w/ turn card")
        self.CalcIfNecessary(2)

    def OnButton6(self,e):
        # check to make sure calculation can be done
        #if self.card_array.count(53) == 0:
        self.title.SetLabel("Showdown")
        self.CalcIfNecessary(3)

    def OnButton4(self,e):
        # reset the card_array
        self.card_array = [53] * 9
        for i in range(len(self.cards)):
            self.cards[i].SetBitmap(catalog[index[53]].getBitmap())
        self.title.SetLabel("")
        self.hand_display.SetLabel("")
        self.hutch_display.SetLabel("")
        self.grid.ClearGrid()
        self.button1.Disable()
        self.button2.Disable()
        self.button3.Disable()
        self.button4.Disable()
        self.button6.Disable()
        if self.minipanel_is_open == 1:
            self.minipanel.ResetSync()

    def OnButton5(self,e):
        button_frame = MyMiniFrame(self, "Button Panel", style=wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION_HORIZ)
        button_frame.SetSize((400,175))
        button_frame.CenterOnParent(wx.BOTH)
        self.button_frame = button_frame
        button_frame.Show(True)

    def OnCellRightClick(self,e):
        row = e.GetRow()
        column = e.GetCol()
        # NOT NEEDED ANYMORE - position of click relative to grid (upper left = 0,0)
        #position = e.GetPosition()
        display_hand_type = 8 - row
        if column == 4 and self.grid.GetCellValue(row,column) != "" and self.grid.GetCellValue(row,column) != "0":
            #print "row %i, column %i, position %s, %s" % (row, column, position, self.hand_type[display_hand_type])
            #print "%s" % self.grid.GetCellValue(row,column)
            popup_string = "** " + self.hand_type[display_hand_type] + " **\n" + self.better[1][display_hand_type][:-1]
            popup = MyTransientPopup(self, wx.SIMPLE_BORDER, popup_string)
            # NOT NEEDED ANYMORE - get the object that was clicked
            #grid = e.GetEventObject()
            # NOT NEEDED ANYMORE - get the position on the screen of the object that was clicked
            #grid_pos = grid.ClientToScreen( (0,0) )
            # popup the window @ the position on the grid offset by the location of the grid on the screen
            # but moved up by the height of the window so that the mouse does not block the text.
	    # NOT NEEDED ANYMORE (following line)
            #popup.Position(position, (grid_pos[0],grid_pos[1]-popup.getHeight()))
	    # The following two lines replaces all of the NOT NEEDED ANYMORE lines.  GetMouseState() is a new feature
	    # that does exactly what I was trying to do.  The popup now works correctly in the second monitor.
	    ms = wx.GetMouseState()
	    popup.Position( (ms.x, ms.y), (0, -popup.getHeight()) )
            popup.Popup()

class MyTransientPopup(wx.PopupTransientWindow):
    def __init__(self, parent, style, text):
        wx.PopupTransientWindow.__init__(self, parent, style)
        self.panel = wx.Panel(self, -1)
        #self.panel.SetBackgroundColour("#FFB6C1")
        st = wx.StaticText(self.panel, -1, text, pos=(10,10))
        #st = wx.StaticText(self.panel, -1, "hello jay\n" "this is the popup\n" "window.", pos=(10,10))
        size = st.GetBestSize()
        self.panel.SetSize( (size.width+20, size.height+20) )
        self.SetSize(self.panel.GetSize())
        #print self, parent

    def getHeight(self):
        return self.panel.GetSize()[1]
        

class MyMiniFrame(wx.MiniFrame):
    def __init__(self, parent, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.MiniFrame.__init__(self, parent, -1, title, pos, size, style)
        myMiniPanel = MyMiniPanel(self)

        self.main_window = parent
        self.main_window.minipanel_is_open = 1
        self.main_window.minipanel = myMiniPanel

        # bind close event to close method that is also used by x
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        #print "OnCloseWindow"
        self.main_window.button5.Enable()
        self.main_window.minipanel_is_open = 0
        self.Destroy()

class MyMiniPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.parent = self.GetParent().GetParent()
        #print self.parent
        self.parent.button5.Disable()

        PANEL_BUTTON_SIZE = (40,10)

        self.button = wx.Button(self, -1, "Close", size=PANEL_BUTTON_SIZE)
        # bind button to close method
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.button)

        self.button2 = wx.Button(self, -1, "Turn")
        self.Bind(wx.EVT_BUTTON, self.parent.OnButton1, self.button2)

        self.button3 = wx.Button(self, -1, "River")
        self.Bind(wx.EVT_BUTTON, self.parent.OnButton2, self.button3)

        self.button4 = wx.Button(self, -1, "River+")
        self.Bind(wx.EVT_BUTTON, self.parent.OnButton3, self.button4)

        self.button6 = wx.Button(self, -1, "Showdown")
        self.Bind(wx.EVT_BUTTON, self.parent.OnButton6, self.button6)

        self.button5 = wx.Button(self, -1, "Reset", size=PANEL_BUTTON_SIZE)
        self.Bind(wx.EVT_BUTTON, self.parent.OnButton4, self.button5)

        spacer_size_a = (3, 1)
        spacer_size_b = (2, 1)
        controlbuttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        controlbuttonsizer.Add(self.button, 0, wx.EXPAND)
        controlbuttonsizer.Add(spacer_size_a, 0, wx.EXPAND)
        controlbuttonsizer.Add(self.button2, 0, wx.EXPAND)
        controlbuttonsizer.Add(spacer_size_b, 0, wx.EXPAND)
        controlbuttonsizer.Add(self.button3, 0, wx.EXPAND)
        controlbuttonsizer.Add(spacer_size_b, 0, wx.EXPAND)
        controlbuttonsizer.Add(self.button4, 0, wx.EXPAND)
        controlbuttonsizer.Add(spacer_size_b, 0, wx.EXPAND)
        controlbuttonsizer.Add(self.button6, 0, wx.EXPAND)
        controlbuttonsizer.Add(spacer_size_a, 0, wx.EXPAND)
        controlbuttonsizer.Add(self.button5, 0, wx.EXPAND)

        mybuttonsizer = wx.GridSizer(4, 13, 5, 5)

        ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
        suits = ('s', 'h', 'd', 'c')

        self.button_array = []
        self.num_buttons_pressed = 0
        self.buttons_are_disabled = 0
        
        for i in range(52):
            label = "%s%s" % (ranks[i%13], suits[i/13])
            b = wx.ToggleButton(self, i, label, size=(25, 25))
            self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle, b)
            mybuttonsizer.Add(b, 0, wx.EXPAND)
            self.button_array.append(b)
            # will also need to toggle buttons for cards that were selected the other way

        # call function to synchronize button panel

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        spacer_size_c = (1, 5)
        self.sizer.Add(spacer_size_c, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.Add(controlbuttonsizer, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.Add(spacer_size_c, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.Add(mybuttonsizer, 0, wx.ALIGN_CENTRE_HORIZONTAL)
        self.sizer.Add(spacer_size_c, 0, wx.ALIGN_CENTRE_HORIZONTAL)

        self.SetSizer(self.sizer)

        # can't call self.parent.SyncWithMini() during initialization because
        # it needs the reference to the object that is being created.
        self.SyncWithMain()
        
    def SyncWithMain(self):
        #print self.parent
        # sync calc buttons
        self.SyncButtons()
        # sync num cards
        self.num_buttons_pressed = 9 - self.parent.card_array.count(53)
        if self.num_buttons_pressed == 9:
            self.buttons_are_disabled = 1
        else:
            self.buttons_are_disabled = 0
        # sync cards
        for i in range(52):
            if self.parent.card_array.count(i) == 1:
                value = True
            else:
                value = False    
            self.button_array[i].SetValue(value)
            if self.num_buttons_pressed == 9:
                self.button_array[i].Enable(value)

    def OnCloseMe(self, event):
        self.GetParent().Close(True)

    def ResetSync(self):
        self.num_buttons_pressed = 0
        for b in self.button_array:
            b.Enable()
            b.SetValue(False)
        self.SyncButtons()

    def SyncButtons(self):
        #print ""
        self.button2.Enable(self.parent.button1.IsEnabled())
        self.button3.Enable(self.parent.button2.IsEnabled())
        self.button4.Enable(self.parent.button3.IsEnabled())
        self.button6.Enable(self.parent.button6.IsEnabled())
        self.button5.Enable(self.parent.button4.IsEnabled())

    def OnToggle(self, e):
        c_index = e.GetId()
        button = e.GetEventObject()
        value = button.GetValue()
        if value == True:
            self.num_buttons_pressed = self.num_buttons_pressed + 1
            # Add the chosen card to the display
            # assume buttons have been sync'd
            # get next card which is still showing a back
            card_to_update = self.parent.card_array.index(53)
            # update the card array
            self.parent.card_array[card_to_update] = c_index
            # update the card display
            self.parent.cards[card_to_update].SetBitmap(catalog[index[c_index]].getBitmap())
        else:
            self.num_buttons_pressed = self.num_buttons_pressed - 1
            # Remove the chosen card from the display
            # need to make button update method take backs into account
            card_to_update = self.parent.card_array.index(c_index)
            # update the card array
            self.parent.card_array[card_to_update] = 53
            # update the card display
            self.parent.cards[card_to_update].SetBitmap(catalog[index[53]].getBitmap())

        #print "buttons pressed = ", self.num_buttons_pressed
        if self.num_buttons_pressed == 9:
            for b in self.button_array:
                if b.GetValue() == False:
                    b.Disable()
            self.buttons_are_disabled = 1
        if self.num_buttons_pressed == 8 and self.buttons_are_disabled == 1:
            for b in self.button_array:
                b.Enable()
            self.buttons_are_disabled = 0

        # update the hand type label
        current_h = self.parent.MinHandEval()
        self.parent.hand_display.SetLabel(current_h)
        # Update hutchison if necessary
        if self.parent.card_array[:4].count(53) == 0:
            h_index = hutchison(self.parent.card_array[:4])
            self.parent.hutch_display.SetLabel(str(h_index))
        else:
            self.parent.hutch_display.SetLabel("")
        # Update buttons on main window - not sure why UpdateButtons gets called with correct "self"
        self.parent.UpdateButtons()
        # sychronize panel buttons
        self.SyncButtons()
        #print self.parent.card_array


class AppFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__( self, None, -1, FRAME_TITLE, size=FRAME_SIZE, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX )
        #wx.Frame.__init__( self, None, -1, FRAME_TITLE, size=FRAME_SIZE, style=wx.DEFAULT_FRAME_STYLE )

        # not sure why i need this line
        self.dirname=''

        # maybe could initialize PNG and ICO handler instead
        wx.InitAllImageHandlers()

        # Put the icon in the title bar
        #icon = wx.EmptyIcon()
        #icon.CopyFromBitmap(wx.Bitmap("frame.ico", wx.BITMAP_TYPE_ICO))
        # The above two lines were used when the icon was a local file.
	icon = frame_icon.getframeIcon()
	self.SetIcon(icon)

        self.CreateStatusBar()
        
        # Create the file menu
        filemenu = wx.Menu()
        filemenu.Append(ID_EXIT, "E&xit", "Terminate the program")

        # Create the help menu
        helpmenu = wx.Menu()
        helpmenu.Append(ID_ABOUT, "&About", "Information about this program")

        # Create the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(helpmenu, "&Help")

        # Add the menubar to the frame
        self.SetMenuBar(menuBar)

        # Attach the menu-event ID_ABOUT to the method self.OnAbout
        self.Bind(wx.EVT_MENU, self.OnAbout, id=ID_ABOUT)
        # Attach the menu-event ID_EXIT to the method self.OnExit)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)

        # Create the calc panel
        self.calcpanel = CalcPanel(self)

        self.Show(1)

    def OnAbout(self,e):
        # Create a message dailog box
	d = wx.MessageDialog(self, "Omaha Odds Calculator v0.2.7\nWritten by Kevin Peterson\nEmail: omahaoddscalculator@gmail.com\n http://www.omahaoddscalculator.com", "About Omaha Odds Calculator", wx.OK)

        # Show it
        d.ShowModal()

        # Destory it when finished
        d.Destroy()

    def OnExit(self,e):
        self.Close(True)    # Close the frame

class MyCalc(wx.App):
	def OnInit(self):
		frame = AppFrame()
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

def main_is_frozen():
    return (hasattr(sys, "frozen"))

if __name__ == '__main__':
    import sys
    import psyco
    
    if len(sys.argv) == 1:
        app = MyCalc(0)
        psyco.full()
        app.MainLoop()
    else:
	if not main_is_frozen():
            psyco.full()
            length = len(sys.argv)
            if length == 2:
                main(sys.argv[1], "", "", "")
            elif length == 3:
                main(sys.argv[1], sys.argv[2], "", "")
            elif length == 4:
                main(sys.argv[1], sys.argv[2], sys.argv[3], "")
            elif length == 5:
                main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
            else:
                # This will never be displayed
                print "Usage: omaha.py <hole_cards> <flop> <turn> <river>"

