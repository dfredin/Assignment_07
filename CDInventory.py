#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Dfredin, 2022-Nov-18, Modified file by adding specific functions
# Dfredin, 2022-Nov-23, Modified file for error handling and use of binary files
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
flag = bool() # boolean flag for file check
import pickle # allows storage to .dat files

# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def add_data(ID, title, artist):
        """Takes the user's input for ID, Title, and artist and appends to table lstTbl.
        
        Args:
            ID (int): integer number that describes the ID for the CD entry.
            title (string): string of the title of the CD.
            artist (string): string of the name of the artist of the CD.

        Returns:
            None.
        """
        try:
            intID = int(ID)
            dicRow = {'ID': intID, 'Title': title, 'Artist': artist}
            lstTbl.append(dicRow)
        except ValueError as e:
            print('\nERROR! Entered ID was not an integer. \nPlease enter an integer ID.\n')
            print(e)
            print()
        
    @staticmethod
    def delete_data(IDdel, table):
        """Deletes the row that the user selcted with IDdel     

        Args:
            IDdel (int): ID of CD row that the user wants deleted.
            table (list of dicts): 2D data structure that holds the rows of CDs in a list.
            
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == IDdel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list of dict): 2D data structure that contains the file data.
        """    
        with open(strFileName, 'rb') as fileObj:
            table = pickle.load(fileObj)
        return table
    
    @staticmethod
    def write_file(file_name, table):
        """Function that overwrites the new data input by the user into the named txt file

        Args:
            file_name (string): name of file used to write the data to.
            table (list): data structure that holds the data during runtime.

        Returns:
            None.
        """        
        with open(strFileName, 'wb') as fileObj:
            pickle.dump(table, fileObj)
        
# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] Load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to file\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def user_input():
        """Gets user input for adding CDs to inventory (ID, title, and artist)
        
        Args:
            None.

        Returns:
            ID (int): an integer the user inputs for CD ID.
            title (string): a string of the CD title name.
            artist (string): a string of the artist's name.
        """        
        ID = input('Enter ID: ').strip()
        title = input('What is the CD\'s title? ').strip()
        artist = input('What is the Artist\'s name? ').strip()
        return ID, title, artist

# 1. When program starts, read in the currently saved Inventory
try:
    lstTbl = FileProcessor.read_file(strFileName, lstTbl) # File not found error handling
except FileNotFoundError as e:
    print('\nERROR! Data file not found! \nAn empty file has now been created.\n')
    print(e)
    print()
    FileProcessor.write_file(strFileName, lstTbl)
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled. ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            try:
                lstTbl = FileProcessor.read_file(strFileName, lstTbl) # File not found error handling
                IO.show_inventory(lstTbl)
            except FileNotFoundError as e:
                print('\nERROR! Data file not found! \nAn empty file has now been created.\n')
                print(e)
                FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, stArtist = IO.user_input()          
        # 3.3.2 Add item to the table       
        DataProcessor.add_data(strID, strTitle, stArtist)    
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove    
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD       
            DataProcessor.delete_data(intIDDel, lstTbl)       
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except ValueError as e:
            print('\nERROR! Entered ID was not an integer. \nPlease enter an integer ID for deletion.\n')
            print(e)
            print() 
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.      
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')