# SQLSEQUEL VER 6 - MULTI TABLE MODE

# MAIN BRANCH

# SQLSEQUEL - A NEW DATABASE LANGUAGE
# THIS SOFTWARE IS BASED LOOSELY OFF OF SQL.
# IT UTILISES A 2D ARRAY CONSISTING OF LISTS WITHIN A LIST.

# I PLAN TO ADD .CSV EXPORT AT A LATER DATE. 
# UPDATE - THIS HAS BEEN REPLACED WITH .txt EXPORTS AND A PARSER.

# INITIALISES 2D ARRAY FOR DATA STORAGE

# TODO (FUTURE ME)

# ADD MODIFYING DIFFERENT TABLES (interpretedCommand[-1]) (COMPLETED)
# UNBUGGER ALL THE PREWRITTEN STUFF (COMPLETED)
# GIVE UP
# QUIT
# RETIRE

# THIS SOFTWARE IS STUPID
# HOURS_WASTED = 20

database = []

importingFlag = 0

autosaveFlag = 0

tableChoice = 0

# DEFINES HEADERS OF TABLE, AND HENCE NUMBER OF COLUMNS

def init():
    global autosaveFlag
    global database
    global importingFlag
    global tableChoice

    # UNTIL A FLAG MANUALLY QUITS THE INITIATION, ADD FIELDS.
    
    while True:
        fieldName = ""        
        
        fieldName = input("Enter the field name, IMPORTTABLE to use an existing table, \
or STOP to stop.")

        fieldName = fieldName.split()[0]
        
        # STOP ADDING RECORDS, PROCEED TO RUNTIME
        
        if fieldName == "STOP":
            break

        # OR WE COULD IMPORT table.txt
        
        if fieldName == "IMPORTTABLE":
            database = []
            importingFlag = 1
            while True:
                importTable()
                if importingFlag == 0:
                    break

        # OTHERWISE, ADD THE FIELD TO THE INDEX ROW
        
        if fieldName != "IMPORTTABLE":

            try:
                tableChoice = int(fieldName.split()[1])
            except Exception as e:
                print("Table choice must be a number.")
                print("Defaulting to table 0.")
                tableChoice = 0

            # CHECK IF THAT TABLE EXISTS
            
            try:
                database[tableChoice]

            # IF NOT
            
            except IndexError:

                # KEEP ADDING TABLES
                
                while True:

                    # ADD A TABLE
                    
                    database.append([[]])

                    # IF WE HAVE IT, EXIT
                    
                    try:
                        database[tableChoice]
                        break

                    # KEEP GOING
                    
                    except IndexError:
                        pass
            
            database[tableChoice][0].append(fieldName)

            # DON'T FORGET TO PAD THE OTHER RECORDS

            for i in range(1, len(database[tableChoice])):
                database[tableChoice][i].append("")

    autosave = input("Would you like to enable autosave for this session? \
Type \"yes\" for yes, and \"no\" for no.")

    if autosave.lower() == "yes":
        autosaveFlag = 1

# IMPORT TABLE

def importTable():

    # OPEN THE FILE OF CHOICE, MAKES SYSTEMS MORE DYNAMIC
    try:
        global database
        global importingFlag

        newTable = []

        tablename = input("What is the filename of your table?")

        if tablename == "STOP":
            importingFlag = 0
            return 0

        tablename = tablename + ".sequel"
        
        f = open(tablename, "rt")
        
        wholeTableString = f.read()
        lineByLine = wholeTableString.splitlines()

        # THIS MAKES A 2D ARRAY FROM THE FILE.
        for i in lineByLine:
            newTable.append(i.split())

        # MAKE SURE THAT EACH RECORD HAS THE SAME NUMBER OF FIELDS AS THE INDEX ROW

        for i in range(1, len(newTable)):

            # IF THE ROW IS SHORTER, ADD SOME FIELDS
            
            if len(newTable[i]) < len(newTable[0]):

                # FOR J IN THE RANGE 0 to DISPARITY IN FIELDS
                
                for j in range(0, (len(newTable[0]) - len(newTable[i]))):
                    # ADD EMPTY TO THE END
                    newTable[i].append("")

            # IF THE ROW IS LONGER, POP FIELD FROM END
            
            if len(newTable[0]) < len(newTable[i]):

                # FOR J IN THE RANGE DISPARITY TO 0
                
                for j in range(len(newTable[i]) - len(newTable[0]), 0, -1):
                    newTable[i].pop(-1)

        database.append(newTable)
        
        f.close()
    
    # NO PRE EXISTING TABLE
    
    except FileNotFoundError:
        print("Table file not found.")
        return 1

    for i in range(0, len(database)):
        print("Table", i)
        for j in range(0, len(database[i])):
            print("Record", j, database[i][j])
            

# ESTABLISHES THE INTERPRETATION VARIABLE

interpretedCommand = ""

# DISPLAYS THE TABLE

def displayTable():
    for i in range(0, len(database)):
        print("Table Number", i, ":")
        for j in range(0, len(database[i])):
            if j == 0:
                print("Index Row:", database[i][j])
            else:
                print("Record Number", j, database[i][j])

# MODIFIES FIELD IN RECORD

def modify():
    global interpretedCommand
    global database
    global tableChoice

    # CHECKS SYNTAX AND ARGUMENTS
    
    try:
        
        if interpretedCommand[2] != "IN":
            print("Syntax Error")
            return 1
        
        # CARRIES OUT RECORD MODIFICATION. CHECKS FOR EXISTENCE OF FIELD.

        try:
            database[tableChoice][int(interpretedCommand[3])][database[tableChoice][0].index(
            interpretedCommand[1])] = interpretedCommand[4]

        # THROWS EXCEPTION
        
        except ValueError:
            print("Field does not exist.")
            return 1
    
    # THROWS EXCEPTION
    
    except IndexError:
        print("Syntax Error. MODIFY (field) IN (record) (content)")
        return 1

# DELETES CONTENT OF DATABASE, EXCLUDING TITLE INDEX

def dropTable():
    global tableChoice
    global database
    for i in range(1, len(database[tableChoice])):
        for j in range(len(database[tableChoice][i])):
            database[tableChoice][i][j] = ""
    return 1

# RETURNS CERTAIN FIELDS

def select():
    global interpretedCommand
    global database
    global tableChoice

    # CHECKS SYNTAX AND ARGUMENTS
    
    try:
        if interpretedCommand[2] != "FROM" and interpretedCommand[2] != "WHERE":
            print("Syntax Error")
            return 1

        # SELECT FIELD IN A RECORD
        
        if interpretedCommand[2] == "FROM":
            if interpretedCommand[1] == "*":
                print(database[tableChoice][int(interpretedCommand[3])])
            else:

                # ATTEMPTS TO RETURN FIELDS
                
                try:
                    print(database[tableChoice][int(interpretedCommand[3])][database[0].index(interpretedCommand[1])])
                
                # THROWS EXCEPTION
                
                except IndexError:
                    print("Field not found.")
                    return 1

        # SELECT RECORDS THAT MEET A SPECIFIC CONDITION
        
        elif interpretedCommand[2] == "WHERE":

            # MAKE A SUB ARRAY TO SIMPLIFY PARSING
    
            evalSubArray = []

            # ADD THE 3 SECTIONS OF THE EVAL SUB ARRAY
            # BY TAKING THE LAST 3 OF THE FULL COMMAND

            # TRY ADDING THE LAST 3
            
            try:
                for i in range(0, 3):
                    evalSubArray.append(interpretedCommand[i + 3])

            except IndexError:
                print("Cannot evaluate condition.", 
                      "Syntax: (field) (== or !=) (content).")
                return 1
            
            try:

                try:

                    # GET THE INDEX OF THE FIELD IN INDEX ROW
                    
                    conditionToCheck = database[tableChoice][0].index(evalSubArray[0])

                # IF IT DOESN'T EXIST
                
                except ValueError:
                    print("Condition does not match database.")
                    return 1

                # MAKE AN ARRAY TO STORE RECORDS MATCHING THE CONDITION
                
                resultsArray = []

                # IF OUR EVAL IS FIELD EQUALS CONTENT:
                
                if evalSubArray[1] == "==":

                    # FOR EVERY ROW IN THE DATABASE
                
                    for i in range(0, len(database[tableChoice])):

                        # CHECK THE FIELD IN THE RECORD AND SEE IF IT EQUALS THE CONTENT
                    
                        if (database[tableChoice][i][conditionToCheck] == 
                            evalSubArray[2]):

                            # ADD THE RECORD TO THE ARRAY IF IT DOES
                        
                            resultsArray.append(i)

                # OR IF THE EVAL IS FIELD NOT EQUALS CONTENT
                
                elif evalSubArray[1] == "!=":

                    # FOR EVERY ROW IN THE DATABASE
                
                    for i in range(0, len(database[tableChoice])):

                        # CHECK THE FIELD IN THE RECORD 
                        # AND SEE IF IT DOESN'T EQUAL THE CONTENT
                    
                        if database[tableChoice][i][conditionToCheck] != evalSubArray[2]:

                            # ADD THE RECORD TO THE ARRAY IF THIS IS TRUE
                        
                            resultsArray.append(i)

                # IF THE OPERATOR ISNT EQUALS OR NOT EQUALS
                
                else:
                    print("Cannot evaluate condition. Use == or !=.")
                    return 1

                # IF THEY WANT THE WHOLE RECORD
                
                if interpretedCommand[1] == "*":

                    for i in resultsArray:

                        # PRINT ALL RECORDS THAT MATCHED OUR CONDITIONS
                
                        print(database[tableChoice][i])

                else:

                    for i in resultsArray:

                        # OR PRINT THE SPECIFIC FIELD THEY ASKED FOR
                        
                        print(database[tableChoice][i][database[0].index(interpretedCommand[1])])

            # IF THE EVAL STRING IS TOO SHORT
            
            except IndexError:
                print("Cannot evaluate condition.", 
                      "Syntax: (field) (== or !=) (content).")
                return 1
    
    # THROWS EXCEPTION IF ANYTHING ELSE IS MISSING
    
    except IndexError:
        print("Syntax Error. SELECT (field) FROM (record),", 
              "or SELECT (field) WHERE (condition)", 
              "Use * to select an entire record.")
        return 1

# ADDS A RECORD TO THE TABLE

def addRecord():
    global tableChoice
    global interpretedCommand
    global database

    # ADDS THE CORRECT NUMBER OF FIELDS TO THE NEW RECORD
    
    database[tableChoice].append([])
    for i in range(len(database[tableChoice][0])):
        database[tableChoice][-1].append("")

# SAVE TABLE

def save():
    global tableChoice
    try:
        fileName = interpretedCommand[1] + ".sequel"
    except IndexError:
        print("Please specify the write location for this table.")
        return 1
    
    # OPENS TABLE STORAGE FILE AND OVERWRITES A BLANK

    f = open(fileName, "wt")
    f.write("")
    f.close()

    # OPENS IN APPEND MODE TO ADD CURRENT DATA

    f = open(fileName, "at")

    # PREVENTS "DATA SHIFTS" BY REPLACING BLANKS WITH NULL.

    for i in range(0, len(database[tableChoice])):
        for j in range(0, len(database[tableChoice][i])):
            if database[tableChoice][i][j] == "":
                database[tableChoice][i][j] = "NULL"

    # FOR THE LENGTH OF THE DATABASE:

    for i in range(0, len(database[tableChoice])):

        # SET THE FIRST PART OF THE STRING TO WRITE

        lineToWrite = str(database[tableChoice][i][0])

        # FOR THE LENGTH OF THE ROW, EXCLUDING FIRST WORD

        for j in range(1, len(database[tableChoice][i])):

            # APPEND TO WRITE CONTAINER

            lineToWrite = lineToWrite + " " + database[tableChoice][i][j]

        # WRITE TO TEXT FILE

        f.write(lineToWrite)

        if i != (len(database[tableChoice]) - 1):
            f.write("\n")

    # TIDY UP

    f.close()

# SEARCH FOR A CERTAIN STRING IN A CERTAIN FIELD

def search():
    global tableChoice
    try:
        if interpretedCommand[1] != "FOR":
            print("Syntax Error. SEARCH FOR (field) (content)")
            return 1

        resultsArray = []
        columnNumber = database[tableChoice][0].index(interpretedCommand[2])
        searchQuery = interpretedCommand[3]

        for i in range(1, len(database[tableChoice])):
            if database[tableChoice][i][columnNumber] == searchQuery:
                resultsArray.append(i)

        print(resultsArray)

    except IndexError:
        print("Syntax Error. SEARCH FOR (field) (content)")
        return 1

# SEARCHES FOR FILLED IN FIELDS

def count():
    global tableChoice
    
    count = 0
    countArray = []
    
    try:

        # INVALID FIELD
        
        if interpretedCommand[1] != "*" and interpretedCommand[1] not in database[tableChoice][0]:
            print("Field not in database.", 
                  "Use * for all fields or use a specific fieldname.")
            return 1

        # IF WE WANT ALL FIELDS COUNTED
        
        if interpretedCommand[1] == "*":

            # FOR EACH COLUMN
            
            for i in range(0, len(database[tableChoice][0])):

                # FOR EACH ROW
                
                for j in range(1, len(database[tableChoice])):
                    
                    # IF DATA IS PRESENT INCREASE THE COUNT
                    if (database[tableChoice][j][i] != "NULL" and
                        database[tableChoice][j][i] != ""):
                        count += 1

                # APPEND IT TO THE LIST
                
                countArray.append(count)

                #RESET FOR NEXT LOOP
                
                count = 0

            print(database[tableChoice][0])
            print(countArray)
            return 0

        else:

            columnToCheck = database[tableChoice][0].index(interpretedCommand[1])

            for i in range(1, len(database[tableChoice])):
                if (database[tableChoice][i][columnToCheck] != "NULL" and 
                    database[tableChoice][i][columnToCheck] != ""):
                    count += 1

            print(database[tableChoice][columnToCheck])
            print(count)
            return 0

    except IndexError:
        print("Syntax Error. Syntax: COUNT (field)")
                    
# LAUNCHES RUNTIME ENVIRONMENT TO RUN COMMANDS IN. LOOPS BACK INTO ITSELF.

def runtime():
    global interpretedCommand
    global tableChoice

    cmd = input()
    interpretedCommand = cmd.split()

    try:
        tableChoice = int(interpretedCommand[-1])
    except Exception as e:
        print("Table number must be a number.")
        print("Defaulting to table 0.")
    
    try:
        if interpretedCommand[0] == "MODIFY":
            modify()
            displayTable()
        elif interpretedCommand[0] == "DROPTABLE":
            dropTable()
            displayTable()
        elif interpretedCommand[0] == "SELECT":
            select()
        elif interpretedCommand[0] == "ADDRECORD":
            addRecord()
            displayTable()
        elif interpretedCommand[0] == "SAVE":
            save()
            displayTable()
        elif interpretedCommand[0] == "SEARCH":
            search()
        elif interpretedCommand[0] == "COUNT":
            count()
        else:
            print("Command Unknown")
    except IndexError:
        print("Command Unknown")

    if autosaveFlag == 1:
        save()

# RUNS THE CODE, BOTH INITIATION AND RUNTIME.

init()

while True:
    runtime()