#Tabular - Library for making tables
#version 2.0 - Emphasis to increase efficiency by reducing the table creation again and again
#it assumes that the minimum size of the table is 2x2
#meant mainly for displaying data though primitive read-write functions are provided


#vertical Table - Titles are at the first row and records are arranged row-wise
#horizontal Table - Titles are at the first column and records are arranged column-wise


import tkinter as tk


#class for making cells (Textbox type)
class Cell:
    def __init__(self, parentTableObject, x, y, valueColumn = None, valueRow = None, bg = 'white', fg = 'black'):

        self.parentTableObject = parentTableObject
        self.parentTable = parentTableObject.Table
        
        self.valueList = parentTableObject.valueList
        self.valueColumn = valueColumn         #index of the value list alloted to the cell
        self.valueRow = valueRow

        self.x_pos = x                      #cell position in the table
        self.y_pos = y

        self.fg = fg       #cell attributes
        self.bg = bg
        self.height = parentTableObject.cellHeight
        self.width = parentTableObject.cellWidth
        self.font = parentTableObject.tblfont

        self.cell_identity = None            #textbox object identity

    #function for making cell
    def makeCell(self):
        self.cell_identity = tk.Text(self.parentTable, fg = self.fg, bg = self.bg, font = self.font, wrap = tk.WORD)
        self.cell_identity.place(x = self.x_pos, y = self.y_pos, height = self.height, width = self.width)

    #function for putting current cell value in value list
    def load_to_index(self):
        #for future - removal of '\n' character from the end using while so that multiple characters can be handled
        self.valueList[self.valueRow][self.valueColumn] = self.cell_identity.get(0.0, tk.END)[:-1]         #trying to remove newline character from end

    #function for loading value from alloted index of valueList
    def load_from_index(self):
        if self.cell_identity.get(1.0, tk.END) != None:
            self.cell_identity.delete(0.0, tk.END)
        
        self.cell_identity.insert(tk.END, self.valueList[self.valueRow][self.valueColumn])

    #shift value position
    def shift_index(self, direction, n = 1):             #direction = 'up'|'down'|'left'|'right', it should be ensured that shifting is possible

        if direction == 'up':
            self.valueRow -= n
        elif direction == 'down':
            self.valueRow += n
        elif direction == 'right':
            self.valueColumn += n
        elif direction == 'left':
            self.valueColumn -= n
        else:
            raise AssertionError('Tabular: shifting direction in cell unvalid.')

        self.load_from_index()

#class for maiking cells of checkcell type
class checkCell(Cell):
    def __init__(self, parentTableObject, x, y, valueColumn = None, valueRow = None, bg = 'white', fg = 'black', text = 'Yes/No'):
        super().__init__(parentTableObject, x, y, valueColumn = valueColumn, valueRow = valueRow, bg = bg, fg = fg)
        self.ivar = tk.IntVar()
        self.text = text

    #overriding function for making cell
    def makeCell(self):
        self.cell_identity = tk.Checkbutton(self.parentTable, fg = self.fg, bg = self.bg,\
             variable = self.ivar, text = self.text)
        self.cell_identity.place(x = self.x_pos, y = self.y_pos)
        #self.cell_identity.grid(column = self.x_pos, row = self.y_pos)    #not proper
        
    #overriding function for putting current cell value in value list
    def load_to_index(self):
        if self.ivar.get() == 1:
            self.valueList[self.valueRow][self.valueColumn] = 'Yes'
        else:
            self.valueList[self.valueRow][self.valueColumn] = 'No'

    #overriding  function for putting current cell values from the index
    def load_from_index(self):

        if self.valueList[self.valueRow][self.valueColumn] == 'Yes':
            self.cell_identity.select()
        else:
            self.cell_identity.deselect()




#class to make table

class Table:
    def __init__(self, parentWindow, tblHeight, tblWidth, tblx, tbly, valueList = [['',''],['','']],\
        tblbg = 'grey15', tblfg = 'white', tblfont = ('Times New Roman', 12),\
        cellbg = 'white', cellfg = 'black', cellHeight = 20, cellWidth = 100, cellspacing = 5,\
        titleRow = False, fixtitleRow = False, titleRowbg = 'purple1', titleRowfg = 'white',\
        titleColumn = False, fixtitleColumn = False, titleColumnbg = 'GreenYellow', titleColumnfg = 'black',\
        tableName = '', readOnly = False, changeOrientation = False, hideButtons = False, cellType = 'Cell',\
        checkCellText = 'Yes/No', leftSpace = 60, rightSpace = 10, topSpace = 10, bottomSpace = 10):


        self.parentWindow = parentWindow
        
        self.valueList = valueList

        self.tblx = tblx
        self.tbly = tbly
        self.tblHeight = tblHeight
        self.tblWidth = tblWidth
        self.tblbg = tblbg
        self.tblfg = tblfg
        self.tblfont = tblfont

        self.cellbg = cellbg
        self.cellfg = cellfg
        self.cellHeight = cellHeight
        self.cellWidth = cellWidth
        self.cellSpacing = cellspacing
        self.cellList = []
        self.cellType = cellType

        self.checkCellText = checkCellText    #used when we use checkCell type

        self.titleRow = titleRow
        self.fixtitleRow = fixtitleRow
        self.titleRowbg = titleRowbg
        self.titleRowfg = titleRowfg
        
        self.titleColumn = titleColumn
        self.fixtitleColumn = fixtitleColumn
        self.titleColumnbg = titleColumnbg
        self.titleColumnfg = titleColumnfg

        self.Table = None
        self.tableName = tableName

        self.table_rows_max = False
        self.table_cols_max = False            #maximum number of columns and rows that can be set in table made

        self.leftSpace = leftSpace
        self.rightSpace = rightSpace
        self.topSpace = topSpace
        self.bottomSpace = bottomSpace              #these are specially calibrated for PEACOCK v1.1, better not to use table Name with that

        if hideButtons == False:
            self.leftSpace = 60

        self.readOnly = readOnly
        self.hideButtons = hideButtons

        if changeOrientation == True:
            self.changeOrientation()
        
        if cellType == 'checkCell':       #special settings for checkCell type
            if self.titleColumn == True:
                self.fixtitleColumn = True
            if self.titleRow == True:
                self.fixtitleRow = True
            
            self.readOnly = True   #since writing options are not available with checkCell type only the check boxes can be read

        self.makeTable()

    #function for making table
    def makeTable(self):

        self.Table = tk.Frame(self.parentWindow,height = self.tblHeight, width = self.tblWidth, bg = self.tblbg)
        self.Table.place(x = self.tblx, y = self.tbly)

        self.decorateTable()

        self.fillcellList()

        #placing values and initialising the cells
        for i in self.cellList:
            for cell in i:
                cell.makeCell()
                cell.load_from_index()

        if self.hideButtons == False:
            self.setButtons()






    #function for loading current values on the table to the valueList
    def submitAction(self):
        for row in self.cellList:
            for cell in row:
                cell.load_to_index()

    #function for loading values from value List
    #function to make the cell List for the first time
    def fillcellList(self):
        maxcols, maxrows = self.findMaxCells()
        valuelistcols, valuelistrows = self.valueList_dimensions()

        if (maxcols <= valuelistcols and maxrows <= valuelistrows):
            self.table_cols_max = True
            self.table_rows_max = True

            temp = []
            xpos = self.leftSpace + self.cellSpacing
            ypos = self.topSpace + self.cellSpacing

            for i in range(maxrows):
                if i != 0:
                    ypos += self.cellSpacing + self.cellHeight

                for j in range(maxcols):
                    if j != 0:
                        xpos += self.cellWidth + self.cellSpacing
                        if i == 0:                           #setting of colours for cell
                            if self.titleRow == True:
                                bg = self.titleRowbg
                                fg = self.titleRowfg
                            else:
                                bg = self.cellbg
                                fg = self.cellfg
                        else:
                            bg = self.cellbg
                            fg = self.cellfg
                    else:
                        xpos = self.leftSpace + self.cellSpacing
                        bg = self.cellbg             #setting of colours
                        fg = self.cellfg
                        if self.titleColumn == True:
                            bg = self.titleColumnbg
                            fg = self.titleColumnfg
                        if self.titleRow == True and i == 0:
                            bg = self.titleRowbg
                            fg = self.titleRowfg
                
                    
                    if self.cellType == 'Cell':
                        temp.append(Cell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg))
                    else:
                        if i != 0 and j != 0:    #especially for checkCell type (if column and row are not 0)
                            temp.append(checkCell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg, text = self.checkCellText))
                        else:
                            if (i == 0 and self.titleRow == True) or (j == 0 and self.titleColumn == True):
                                temp.append(Cell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg))     #from title point of view
                            else:
                                temp.append(checkCell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg, text = self.checkCellText))


                self.cellList.append(list(temp))
                temp.clear()

        elif (maxcols > valuelistcols and maxrows <= valuelistrows):
            self.table_cols_max = False
            self.table_rows_max = True

            temp = []
            xpos = self.leftSpace + self.cellSpacing
            ypos = self.topSpace + self.cellSpacing

            for i in range(maxrows):
                if i != 0:
                    ypos += self.cellSpacing + self.cellHeight

                for j in range(valuelistcols):
                    if j != 0:
                        xpos += self.cellWidth + self.cellSpacing
                        if i == 0:                           #setting of colours for cell
                            if self.titleRow == True:
                                bg = self.titleRowbg
                                fg = self.titleRowfg
                            else:
                                bg = self.cellbg
                                fg = self.cellfg
                        else:
                            bg = self.cellbg
                            fg = self.cellfg
                    else:
                        xpos = self.leftSpace + self.cellSpacing
                        bg = self.cellbg                #setting of colours
                        fg = self.cellfg
                        if self.titleColumn == True:
                            bg = self.titleColumnbg
                            fg = self.titleColumnfg
                        if self.titleRow == True and i == 0:
                            bg = self.titleRowbg
                            fg = self.titleRowfg
      

                    if self.cellType == 'Cell':
                        temp.append(Cell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg))
                    else:
                        if i != 0 and j != 0:    #especially for checkCell type (if column and row are not 0)
                            temp.append(checkCell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg, text = self.checkCellText))
                        else:
                            if (i == 0 and self.titleRow == True) or (j == 0 and self.titleColumn == True):
                                temp.append(Cell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg))     #from title point of view
                            else:
                                temp.append(checkCell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg, text = self.checkCellText))

                self.cellList.append(list(temp))
                temp.clear()

        elif (maxcols <= valuelistcols and maxrows > valuelistrows):
            self.table_cols_max = True
            self.table_rows_max = False

            temp = []
            xpos = self.leftSpace + self.cellSpacing
            ypos = self.topSpace + self.cellSpacing

            for i in range(valuelistrows):
                if i != 0:
                    ypos += self.cellSpacing + self.cellHeight

                for j in range(maxcols):
                    if j != 0:
                        xpos += self.cellWidth + self.cellSpacing
                        if i == 0:                           #setting of colours for cell
                            if self.titleRow == True:
                                bg = self.titleRowbg
                                fg = self.titleRowfg
                            else:
                                bg = self.cellbg
                                fg = self.cellfg
                        else:
                            bg = self.cellbg
                            fg = self.cellfg
                    else:
                        xpos = self.leftSpace + self.cellSpacing
                        bg = self.cellbg                      #setting of colours
                        fg = self.cellfg
                        if self.titleColumn == True:
                            bg = self.titleColumnbg
                            fg = self.titleColumnfg
                        if self.titleRow == True and i == 0:
                            bg = self.titleRowbg
                            fg = self.titleRowfg
      


                    if self.cellType == 'Cell':
                        temp.append(Cell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg))
                    else:
                        if i != 0 and j != 0:    #especially for checkCell type (if column and row are not 0)
                            temp.append(checkCell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg, text = self.checkCellText))
                        else:
                            if (i == 0 and self.titleRow == True) or (j == 0 and self.titleColumn == True):
                                temp.append(Cell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg))     #from title point of view
                            else:
                                temp.append(checkCell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg, text = self.checkCellText))
                    
                self.cellList.append(list(temp))
                temp.clear()
            
        else:
            self.table_cols_max = False
            self.table_rows_max = False

            temp = []
            xpos = self.leftSpace + self.cellSpacing
            ypos = self.topSpace + self.cellSpacing
            bg, fg = 'black', 'white'

            for i in range(valuelistrows):
                if i != 0:
                    ypos += self.cellSpacing + self.cellHeight


                for j in range(valuelistcols):
                    if j != 0:
                        xpos += self.cellWidth + self.cellSpacing
                        if i == 0:
                            if self.titleRow == True:
                                bg = self.titleRowbg
                                fg = self.titleRowfg
                            else:
                                bg = self.cellbg
                                fg = self.cellfg
                        else:
                            bg = self.cellbg
                            fg = self.cellfg

                    else:
                        xpos = self.leftSpace + self.cellSpacing
                        bg = self.cellbg
                        fg = self.cellfg
                        if self.titleColumn == True:
                            bg = self.titleColumnbg
                            fg = self.titleColumnfg
                        if self.titleRow == True and i == 0:
                            bg = self.titleRowbg
                            fg = self.titleRowfg
      
                    if self.cellType == 'Cell':
                        temp.append(Cell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg))
                    else:
                        if i != 0 and j != 0:    #especially for checkCell type (if column and row are not 0)
                            temp.append(checkCell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg, text = self.checkCellText))
                        else:
                            if (i == 0 and self.titleRow == True) or (j == 0 and self.titleColumn == True):
                                temp.append(Cell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg))     #from title point of view
                            else:
                                temp.append(checkCell(self, x = xpos, y = ypos, valueColumn = j, valueRow = i, bg = bg, fg = fg, text = self.checkCellText))
                self.cellList.append(list(temp))
                temp.clear()

        
    #function for shifting values in cell i.e. shifting table
    def shiftTable(self, direction, n = 1):        #direction = up|down|left|right
        self.submitAction()
        if direction == 'up':
            #shifting only if possible
            if self.fixtitleRow == False:
                if self.cellList[0][0].valueRow > 0:
                    for i in self.cellList:
                        for cell in i:
                            cell.shift_index('up', n)
            else:      #fixtitleRow == True
                if self.cellList[1][0].valueRow > 1:
                    for i in self.cellList[1:]:
                        for cell in i:
                            cell.shift_index('up', n)

        elif direction == 'down':
            #shifting only if possible
            if self.fixtitleRow == False:
                if self.cellList[-1][0].valueRow < (len(self.valueList) - 1):
                    for i in self.cellList:
                        for cell in i:
                            cell.shift_index('down', n)
            else:          #fixtitleRow == True
                if self.cellList[-1][0].valueRow < (len(self.valueList) - 1):
                    for i in self.cellList[1:]:
                        for cell in i:
                            cell.shift_index('down', n)                

        elif direction == 'right':
            #shifting only if possible
            if self.fixtitleColumn == False:
                if self.cellList[0][-1].valueColumn < (len(self.valueList[0]) -1):
                    for i in self.cellList:
                        for cell in i:
                            cell.shift_index('right', n)
            else:
                if self.cellList[0][-1].valueColumn < (len(self.valueList[0]) -1):
                    for i in self.cellList:
                        for cell in i[1:]:
                            cell.shift_index('right', n)
                    
        elif direction == 'left':
            #shifting only if possible
            if self.fixtitleColumn == False:
                if self.cellList[0][0].valueColumn > 0:
                    for i in self.cellList:
                        for cell in i:
                            cell.shift_index('left')
            else:
                if self.cellList[0][1].valueColumn > 1:
                    for i in self.cellList:
                        for cell in i[1:]:
                            cell.shift_index('left')
        else:
            raise AssertionError('Tabular: Table.shiftTable(): unvalid direction')
                        

    #funciton for placing buttons in the frame
    def setButtons(self):

        #table shifting buttons
        leftShift_button = tk.Button(self.Table, text = '<', font = ('Calibri', 12, 'bold'), bg = self.tblbg, fg = self.tblfg, command = lambda: self.shiftTable('left'))
        rightShift_button = tk.Button(self.Table, text = '>', font = ('Calibri', 12, 'bold'), bg = self.tblbg, fg = self.tblfg,  command = lambda: self.shiftTable('right'))
        upShift_button = tk.Button(self.Table, text = '^', font = ('Calibri', 12,'bold'), bg = self.tblbg, fg = self.tblfg,  command = lambda: self.shiftTable('up'))
        downShift_button = tk.Button(self.Table, text = 'v', font = ('Calibri', 12, 'bold'), bg = self.tblbg, fg = self.tblfg,  command = lambda: self.shiftTable('down'))
        home_button = tk.Button(self.Table, bg = self.tblbg, fg = self.tblfg,  command = self.home_button_function)
        
        leftShift_button.place(x = 1, y = (21 + self.topSpace), height = 20, width = 20)
        rightShift_button.place(x = 41, y = (21 + self.topSpace), height = 20, width = 20)
        upShift_button.place(x = 21, y = (1 + self.topSpace), height = 20, width = 20)
        downShift_button.place(x = 21, y = (41 + self.topSpace), height = 20, width = 20)
        home_button.place(x = 21, y = (21 + self.topSpace), height = 20, width = 20)

        #buttons for writing operations
        if self.readOnly == False:
            insert_Label = tk.Label(self.Table, text = 'Insert -',  bg = self.tblbg, fg = self.tblfg, font = ('Calibri', 12))
            insert_Label.place(x = 5, y = self.topSpace + 71)

            insertRow_Button = tk.Button(self.Table, text = 'Row', bg = self.tblbg, fg = self.tblfg, command = self.insertRow)
            insertCol_Button = tk.Button(self.Table, text = 'Column', bg = self.tblbg, fg = self.tblfg, command = self.insertColumn)

            insertRow_Button.place(x = 5, y = self.topSpace + 92, width = 50, height = 20)
            insertCol_Button.place(x = 5, y = self.topSpace + 114, width = 50, height = 22)

    #function for home button
    def home_button_function(self):
        self.submitAction()
        for i in range(len(self.cellList)):
            for j in range(len(self.cellList[i])):
                self.cellList[i][j].valueColumn = j
                self.cellList[i][j].valueRow = i

        for i in self.cellList:
            for cell in i:
                cell.load_from_index()


    #funciton for changing orientation           copied from v1.1
    def changeOrientation(self):
        flippedlist = []
        for i in self.valueList:
            for j in i:
                flippedlist.append([])            #since number of rows in flipped list = number of columns in main list
            break

        count = -1
        for i in flippedlist:             #converting the columns of valueList into rows in flippedlist
            count += 1
            for j in self.valueList:
                i.append(j[count])           

        self.valueList = list(flippedlist)        #so that the addresses for both the list are different
        del flippedlist 
    
    #function for finding the maximum number rows and colunms that can be made from cells in the table
    def findMaxCells(self):
        xlength = self.tblWidth - (self.leftSpace + self.rightSpace)
        ylength = self.tblHeight - (self.topSpace + self.bottomSpace)

        maxcols = xlength // (self.cellWidth + self.cellSpacing)
        maxrows = ylength // (self.cellHeight + self.cellSpacing)

        #print('maxcols = ', maxcols, 'maxrows = ', maxrows)      #only for debugging purposes
        return maxcols, maxrows

    #value for finding the dimensions of the valueList
    def valueList_dimensions(self):
        cols = rows = 0

        for i in self.valueList:
            rows += 1
            if rows == 1:
                for j in i:
                    cols += 1            #we need to count the number of columns only once

        #print('cols = ', cols, 'rows = ', rows)  #for debugging purposes only

        return cols, rows


    #function to insert row (designed to insert only one row)
    def insertRow(self):
        valuecols, valuerows = self.valueList_dimensions()

        temp = []
        for i in range(valuecols):
            temp.append('')
        
        self.valueList.append(temp)       #row inserted in valueList

        #making rows if no. of rows is less than maximum rows of cells available
        if self.table_rows_max == False:
            valuecols, valuerows = self.valueList_dimensions()
            maxcols, maxrows = self.findMaxCells()
            if (maxrows - valuerows) == 0:
                self.table_rows_max = True

            lst = []
            xpos = self.leftSpace + self.cellSpacing
            ypos = self.topSpace + ((valuerows - 1) * (self.cellSpacing + self.cellHeight)) + self.cellSpacing
            for i in range(len(self.cellList[0])):
                if self.cellType == 'Cell':
                    lst.append(Cell(self, x = xpos, y = ypos, valueColumn = i, valueRow = (valuerows - 1), bg = self.cellList[-1][i].bg , fg = self.cellList[-1][i].fg))
                else:
                    lst.append(checkCell(self, x = xpos, y = ypos, valueColumn = i, valueRow = (valuerows - 1), bg = self.cellList[-1][i].bg , fg = self.cellList[-1][i].fg,\
                        text = self.checkCellText))
                xpos += (self.cellWidth + self.cellSpacing)

            for cell in lst:
                cell.makeCell()
                cell.load_from_index()
            
            self.cellList.append(lst)
        
        #self.shiftTable('down')           #just for show, it has nothing to do with inserting          (not safe now because it shifts more than limit at ends)

    #function inserting Columns (designed to insert only one column)
    def insertColumn(self):
        valuecols, valuerows = self.valueList_dimensions()

        for i in range(valuerows):
            self.valueList[i].append('')

        #making columns if no. of cols is less than maximum cols of cell available
        if self.table_cols_max == False:
            valuecols, valuerows = self.valueList_dimensions()
            maxcols, maxrows = self.findMaxCells()
            if (maxcols - valuecols) == 0:
                self.table_cols_max = True
            
            ypos = self.topSpace + self.cellSpacing
            xpos = self.leftSpace + ((self.cellWidth + self.cellSpacing) * (valuecols - 1)) + self.cellSpacing

            for i in range(len(self.cellList)):
                if self.cellType == 'Cell':
                    self.cellList[i].append(Cell(self, x = xpos, y = ypos, valueColumn= (valuecols - 1), valueRow= i, bg = self.cellList[i][-1].bg, fg = self.cellList[i][-2].fg))
                else:
                    self.cellList[i].append(checkCell(self, x = xpos, y = ypos, valueColumn= (valuecols - 1), valueRow= i, bg = self.cellList[i][-1].bg, fg = self.cellList[i][-2].fg,\
                        text = self.checkCellText))
                ypos += self.cellSpacing + self.cellHeight
            
            for row in self.cellList:
                row[-1].makeCell()
                row[-1].load_from_index()

        #self.shiftTable('right')         #just for show, it has nothing to do with inserting actually      (not safe because it shifts more at the ends)

    #function for updating of table with new valueList
    def updateTable(self, newValueList, changeOrientation = False):
        self.valueList = newValueList
        if changeOrientation == True:
            self.changeOrientation()
        self.Table.destroy()
        self.cellList.clear()
        self.makeTable()

    #function to return self.valueList along with the orientation(depending on titleRow and titleColumn), default orientation is vertical
    def getTableData(self, pdc = False, orient = None):           #pdc identifies whether the data is to be returned in pdc (peacock dictionary) format
        self.submitAction()
        
        if pdc == True:
            if orient == None:
                if self.titleRow == True:      #if the row is set as title Row
                    orient = 'vertical'
                elif self.titleColumn == True:
                    orient = 'horizontal'
                else:     #default
                    orient = 'vertical'
            
            return table_to_pdc(self.valueList, orient= orient)  #note: orient refers to the orientation of table here

        else:
            
            return self.valueList

    #function for setting show on the table
    def decorateTable(self):
        if self.tableName != '':
            name_Label = tk.Label(self.Table, text = ('TABLE: ' + self.tableName), font = ('Times New Roman', 15, 'bold'), fg = self.tblfg, bg = self.tblbg)
            name_Label.place(x = self.leftSpace, y = 2)

        #mark_Label = tk.Label(self.Table, text = 'TABULAR', font = ('Times New Roman', 10, 'bold'), fg = self.tblfg, bg = self.tblbg)
        #mark_Label.place(x = (self.tblWidth - 70), y = (self.tblHeight - self.bottomSpace + 2))                               #removed especially for peacock

    #function for destroying/removing the table
    def remove(self):
        self.Table.destroy()

    #function for griding the table
    def grid(self,**kwargs):
        self.Table.grid(**kwargs)
    
#function for converting a list of dictionaries into horizontally and vertically oriented tables (lists)
#(Note: This function assumes that each member dictionary has unique keys as each member record can have only one value for each attribute in reality, however
# the value for first occurence of key is taken if the key is repeated in the record.)
def pdc_to_table(dictlist, orient = 'vertical'):           #orient = vertical|horizontal, pdc means peacock dictionary

    no_of_Records = 0
    #obtaining all the available keys
    keylist = []
    for dictionary in dictlist:
        no_of_Records += 1
        for key in dictionary.keys():
            if key not in keylist:
                keylist.append(key)
    
    if orient == 'vertical':         #first row is the title row
        table_list = []          #the final list
        
        for i in range(no_of_Records + 1): # 1 extra list for title row
            table_list.append([])
        
        for key in keylist:

            table_list[0].append(key)

            count = 0
            for i in dictlist:               #searching all the dictionaries for the key its value
                count += 1
                if key in i.keys():
                    table_list[count].append(str(i[key]))         #append the value if present
                else:
                    table_list[count].append('')
        return table_list

    elif orient == 'horizontal':          #first column is the title column
        table_list = []

        for i in range(len(keylist)):       #since, the number of columns depend on the number of keys here    
            table_list.append([])            #empty list with lists equal to the total number of records

        count = -1
        for key in keylist:
            count += 1
            
            table_list[count].append(key)

            for i in dictlist:             #searching key in every dictionary
                if key in i.keys():
                    table_list[count].append(str(i[key]))
                else:
                    table_list[count].append('')
            
        return table_list

    else:
        raise AssertionError('Tabular.dict_to_table: orient can take only on of the values- "horizontal" or "vertical"')
        return []



def table_to_pdc(tablelist, orient = 'vertical'):      #orient = vertical|horizontal, tablelist is of the form of the Table.valueList, and 
                                                       #orient refers to the orientation of the table
    pdcList = []

    if orient == 'vertical':
        count = -1
        for i in tablelist:
            count += 1
            if count != 0:
                tempdict = {}
                for j in range(len(i)):
                    if i[j] != '':
                        print(i,j)      #debugging
                        tempdict[tablelist[0][j]] = i[j]
                pdcList.append(tempdict)
        return pdcList

    elif orient == 'horizontal':
        for i in tablelist:
            for j in range(1, len(i)):      #no. of records == (no. of columns - 1)
                pdcList.append({})
            break

        count = -1     
        for row in tablelist:
            count += 1
            for j in range(1, len(row)):
                if row[j] != '':
                    pdcList[j-1][row[0]] = row[j]
        return pdcList
    
    else:
        raise AssertionError('Tabular:table_to_pdc: invalid orientation given.')
        return []



#version = '2.0.5'
#completed on 2 April 2020        

#version = '2.0.6'  # (debugging of getTableData and table_to_pdc for orient)
#completed on 24 April 2020
#a note on performance
#Performance is good when there are approximately 200 - 250 cells on the screen. (as tested on Intel Pentium Silver J5005 @ 1.50 GHz and ~ 4 GB of RAM)
#there is virtually no limit on the size of valueList (it completely depends on the hardware) though, it was 10 million list elements on this processor. Recommended - 1 million.


#version = '2.1.1'
#release note - adds the checkCell functionality to cells (Inserting rows and columns is not possible, they can only be given as a sheet to be filled)
#completed on 30 April 2020

#version = '2.2.0'
#release note - adds shifting n rows and n columns to shifttable function though the default table buttons to shift by n = 1

version = '2.2.1'
#release note - addition of grid function for the table

