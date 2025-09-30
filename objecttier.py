#
# objecttier
#
# Builds Lobbyist-related objects from data retrieved through 
# the data tier.
#

import datatier


##################################################################
#
# Lobbyist:
#
# Constructor(...)
# Properties:
#   Lobbyist_ID: int
#   First_Name: string
#   Last_Name: string
#   Phone: string
#
class Lobbyist:
  def __init__(self, Lobbyist_ID, First_Name, Last_Name, Phone):
    self._Lobbyist_ID = Lobbyist_ID
    self._First_Name = First_Name
    self._Last_Name = Last_Name
    self._Phone = Phone

  @property
  def Lobbyist_ID(self):
      return self._Lobbyist_ID

  @property
  def First_Name(self):
      return self._First_Name

  @property
  def Last_Name(self):
      return self._Last_Name

  @property
  def Phone(self):
      return self._Phone

##################################################################
#
# LobbyistDetails:
#
# Constructor(...)
# Properties:
#   Lobbyist_ID: int
#   Salutation: string
#   First_Name: string
#   Middle_Initial: string
#   Last_Name: string
#   Suffix: string
#   Address_1: string
#   Address_2: string
#   City: string
#   State_Initial: string
#   Zip_Code: string
#   Country: string
#   Email: string
#   Phone: string
#   Fax: string
#   Years_Registered: list of years
#   Employers: list of employer names
#   Total_Compensation: float
#
class LobbyistDetails:
  def __init__(self, Lobbyist_ID, Salutation, First_Name, Middle_Initial, Last_Name, Suffix, Address_1, Address_2, City, State_Initial, Zip_Code, Country, Email, Phone, Fax, Years_Registered, Employers, Total_Compensation):
    self._Lobbyist_ID = Lobbyist_ID
    self._Salutation = Salutation
    self._First_Name = First_Name
    self._Middle_Initial = Middle_Initial
    self._Last_Name = Last_Name
    self._Suffix = Suffix
    self._Address_1 = Address_1
    self._Address_2 = Address_2
    self._City = City
    self._State_Initial = State_Initial
    self._Zip_Code = Zip_Code
    self._Country = Country
    self._Email = Email
    self._Phone = Phone
    self._Fax = Fax
    self._Years_Registered = Years_Registered
    self._Employers = Employers
    self._Total_Compensation = Total_Compensation

  @property
  def Lobbyist_ID(self):
    return self._Lobbyist_ID

  @property
  def Salutation(self):
    return self._Salutation

  @property
  def First_Name(self):
    return self._First_Name

  @property
  def Middle_Initial(self):
    return self._Middle_Initial

  @property
  def Last_Name(self):
    return self._Last_Name

  @property
  def Suffix(self):
    return self._Suffix

  @property
  def Address_1(self):
    return self._Address_1

  @property
  def Address_2(self):
    return self._Address_2

  @property
  def City(self):
    return self._City

  @property
  def State_Initial(self):
    return self._State_Initial

  @property
  def Zip_Code(self):
    return self._Zip_Code

  @property
  def Country(self):
    return self._Country

  @property
  def Email(self):
    return self._Email

  @property
  def Phone(self):
    return self._Phone

  @property
  def Fax(self):
    return self._Fax

  @property
  def Years_Registered(self):
    return self._Years_Registered

  @property
  def Employers(self):
    return self._Employers

  @property
  def Total_Compensation(self):
    return self._Total_Compensation



##################################################################
#
# LobbyistClients:
#
# Constructor(...)
# Properties:
#   Lobbyist_ID: int
#   First_Name: string
#   Last_Name: string
#   Phone: string
#   Total_Compensation: float
#   Clients: list of clients
#
class LobbyistClients:
  def __init__(self, Lobbyist_ID, First_Name, Last_Name, Phone, Total_Compensation, Clients):
    self._Lobbyist_ID = Lobbyist_ID
    self._First_Name = First_Name
    self._Last_Name = Last_Name
    self._Phone = Phone
    self._Total_Compensation = Total_Compensation
    self._Clients = Clients

  @property
  def Lobbyist_ID(self):
    return self._Lobbyist_ID

  @property
  def First_Name(self):
    return self._First_Name

  @property
  def Last_Name(self):
    return self._Last_Name

  @property
  def Phone(self):
    return self._Phone

  @property
  def Total_Compensation(self):
    return self._Total_Compensation

  @property
  def Clients(self):
    return self._Clients

##################################################################
# 
# num_lobbyists:
#
# Returns: number of lobbyists in the database
#           If an error occurs, the function returns -1
#
def num_lobbyists(dbConn):
  #counts the number of lobbyists in the database
  sql_query = "SELECT COUNT(*) FROM LobbyistInfo"

  #gets tupple of number of lobbyists
  result = datatier.select_one_row(dbConn, sql_query, None)
  if result is None:
    return -1 #if there is an error, return -1
  
  return result[0]
  
##################################################################
# 
# num_employers:
#
# Returns: number of employers in the database
#           If an error occurs, the function returns -1
#
def num_employers(dbConn):
  #counts number of employers in the database
  sql_query = "SELECT COUNT(*) FROM EmployerInfo"

  #gets tupple of number of employers
  result = datatier.select_one_row(dbConn, sql_query, None)
  if result is None:
    return -1
  return result[0]

##################################################################
# 
# num_clients:
#
# Returns: number of clients in the database
#           If an error occurs, the function returns -1
#
def num_clients(dbConn):
  #gets number of clients in the database
  sql_query = "SELECT COUNT(*) FROM ClientInfo"

  #gets tupple of number of clients
  result = datatier.select_one_row(dbConn, sql_query, None)
  if result is None:
    return -1
  return result[0]

##################################################################
#
# get_lobbyists:
#
# gets and returns all lobbyists whose first or last name are "like"
# the pattern. Patterns are based on SQL, which allow the _ and % 
# wildcards.
#
# Returns: list of lobbyists in ascending order by ID; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_lobbyists(dbConn, pattern):
  #gets all lobbyists whose first or last name are "like" the pattern(first or last name))
  sql_query = "SELECT Lobbyist_ID, First_Name, Last_Name, Phone FROM LobbyistInfo WHERE First_Name LIKE ? OR Last_Name LIKE ? ORDER BY Lobbyist_ID ASC"
  parameters = (pattern, pattern)
  
  results = datatier.select_n_rows(dbConn, sql_query, parameters)

  #stores results in a list and returns it
  lobbyists = []
  for row in results:
    lobbyist = Lobbyist(row[0], row[1], row[2], row[3])
    lobbyists.append(lobbyist)
  return lobbyists


##################################################################
#
# get_lobbyist_details:
#
# gets and returns details about the given lobbyist
# the lobbyist id is passed as a parameter
#
# Returns: if the search was successful, a LobbyistDetails object
#          is returned. If the search did not find a matching
#          lobbyist, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_lobbyist_details(dbConn, lobbyist_id):

  #gets all the employers given lobbyist id
  sql_query_employers = "SELECT DISTINCT EmployerInfo.Employer_Name FROM EmployerInfo LEFT JOIN LobbyistAndEmployer ON EmployerInfo.Employer_ID = LobbyistAndEmployer.Employer_ID JOIN LobbyistInfo ON LobbyistInfo.Lobbyist_ID = LobbyistAndEmployer.Lobbyist_ID WHERE LobbyistInfo.Lobbyist_ID = ? ORDER BY EmployerInfo.Employer_Name ASC"
  parameters_e = (lobbyist_id,)
  employer_results = datatier.select_n_rows(dbConn, sql_query_employers, parameters_e)
  employers = [row[0] for row in employer_results] #puts employers in a list

  #gets lobbyists details given the lobbyist ids
  sql_query = """
      SELECT LobbyistInfo.Lobbyist_ID,
             LobbyistInfo.Salutation,
             LobbyistInfo.First_Name,
             LobbyistInfo.Middle_Initial,
             LobbyistInfo.Last_Name,
             LobbyistInfo.Suffix,
             LobbyistInfo.Address_1,
             LobbyistInfo.Address_2,
             LobbyistInfo.City,
             LobbyistInfo.State_Initial,
             LobbyistInfo.ZipCode,
             LobbyistInfo.Country,
             LobbyistInfo.Email,
             LobbyistInfo.Phone,
             LobbyistInfo.Fax,
             LobbyistYears.Year AS Years_Registered,
             COALESCE(SUM(Compensation.Compensation_Amount), 0) AS total_compensation
      FROM LobbyistInfo
      LEFT JOIN LobbyistYears ON LobbyistYears.Lobbyist_ID = LobbyistInfo.Lobbyist_ID
      LEFT JOIN Compensation ON Compensation.Lobbyist_ID = LobbyistInfo.Lobbyist_ID
      WHERE LobbyistInfo.Lobbyist_ID = ? 
      GROUP BY LobbyistYears.Year ORDER BY LobbyistYears.Year ASC
  """
  
  parameters = (lobbyist_id,)
  result = datatier.select_n_rows(dbConn, sql_query, parameters)
  if result == []:
    return None
  else:
    years = [row[15] for row in result] #stores years in a list
    lobby_details = LobbyistDetails(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7], result[0][8], result[0][9], result[0][10],result[0][11], result[0][12], result[0][13], result[0][14], years, employers, result[0][16])
    return lobby_details
    

         

##################################################################
#
# get_top_N_lobbyists:
#
# gets and returns the top N lobbyists based on their total 
# compensation, given a particular year
#
# Returns: returns a list of 0 or more LobbyistClients objects;
#          the list could be empty if the year is invalid. 
#          An empty list is also returned if an internal error 
#          occurs (in which case an error msg is already output).
#
def get_top_N_lobbyists(dbConn, N, year):
  #gets the id, name, and phone number, and compensation for client details
  sql_query = """
      SELECT
          LobbyistInfo.Lobbyist_ID,
          LobbyistInfo.First_Name,
          LobbyistInfo.Last_Name,
          LobbyistInfo.Phone,
          COALESCE(SUM(Compensation.Compensation_Amount), 0) AS total_compensation
      FROM
          LobbyistInfo
          JOIN LobbyistYears ON LobbyistInfo.Lobbyist_ID = LobbyistYears.Lobbyist_ID
          JOIN Compensation ON LobbyistInfo.Lobbyist_ID = Compensation.Lobbyist_ID
      WHERE
          LobbyistYears.Year = ?
          AND strftime('%Y', Compensation.Period_Start) = ?
          AND strftime('%Y', Compensation.Period_End) = ?
      GROUP BY
          LobbyistInfo.Lobbyist_ID,
          LobbyistInfo.First_Name,
          LobbyistInfo.Last_Name,
          LobbyistInfo.Phone
      ORDER BY
          total_compensation DESC,
          LobbyistInfo.Last_Name ASC
      LIMIT ?
  """

  # Execute main query to get top N lobbyists
  parameters_main = (year, year, year, N)
  result_main = datatier.select_n_rows(dbConn, sql_query, parameters_main)

  lobbyists = []
  for row in result_main:
    lobbyist_id = row[0]
    first_name = row[1]
    last_name = row[2]
    phone = row[3]
    total_compensation = row[4]

      # Fetch distinct client names for the current lobbyist
    sql_query_clients = """
        SELECT DISTINCT ClientInfo.Client_ID, ClientInfo.Client_Name
        FROM Compensation
        JOIN ClientInfo ON Compensation.Client_ID = ClientInfo.Client_ID
        JOIN LobbyistInfo ON LobbyistInfo.Lobbyist_ID = Compensation.Lobbyist_ID
        JOIN LobbyistYears ON LobbyistInfo.Lobbyist_ID = LobbyistYears.Lobbyist_ID
        WHERE LobbyistInfo.Lobbyist_ID = ?
            AND LobbyistYears.Year = ?
            AND strftime('%Y', Compensation.Period_Start) = ?
            AND strftime('%Y', Compensation.Period_End) = ?
        ORDER BY ClientInfo.Client_Name
    """
    parameters_clients = (lobbyist_id, year, year, year)
    clients_result = datatier.select_n_rows(dbConn, sql_query_clients, parameters_clients)

    # Extract client names from the result set and puts in a list
    clients = [row[1] for row in clients_result]

    # Create LobbyistClients object and append to list
    lobbyist = LobbyistClients(lobbyist_id, first_name, last_name, phone, total_compensation, clients)
    lobbyists.append(lobbyist)

  return lobbyists

##################################################################
#
# add_lobbyist_year:
#
# Inserts the given year into the database for the given lobbyist.
# It is considered an error if the lobbyist does not exist (see below), 
# and the year is not inserted.
#
# Returns: 1 if the year was successfully added,
#          0 if not (e.g. if the lobbyist does not exist, or if
#          an internal error occurred).
#
def add_lobbyist_year(dbConn, lobbyist_id, year):
  # Check if the lobbyist exists
  check_sql = "SELECT Lobbyist_ID FROM LobbyistInfo WHERE Lobbyist_ID = ?"
  parameters = (lobbyist_id,)
  result = datatier.select_one_row(dbConn, check_sql, parameters)
  if result == ():
    return 0
  
  # Insert the year for the lobbyist
  insert_sql = "INSERT INTO LobbyistYears (lobbyist_id, year) VALUES (?, ?)"
  action_parameters = (lobbyist_id, year)
  rows_modified = datatier.perform_action(dbConn, insert_sql, action_parameters)

  #if successful return 1 else 0
  if rows_modified > 0:
    return 1
  else:
    return 0


##################################################################
#
# set_salutation:
#
# Sets the salutation for the given lobbyist.
# If the lobbyist already has a salutation, it will be replaced by
# this new value. Passing a salutation of "" effectively 
# deletes the existing salutation. It is considered an error
# if the lobbyist does not exist (see below), and the salutation
# is not set.
#
# Returns: 1 if the salutation was successfully set,
#          0 if not (e.g. if the lobbyist does not exist, or if
#          an internal error occurred).
#
def set_salutation(dbConn, lobbyist_id, salutation):
  check_sql = "SELECT Lobbyist_ID FROM LobbyistInfo WHERE Lobbyist_ID = ?"
  parameters = (lobbyist_id,)
  result = datatier.select_one_row(dbConn, check_sql, parameters)

  if result is None:
    return 0

  # Update the salutation for the lobbyist
  update_sql = "UPDATE LobbyistInfo SET salutation = ? WHERE Lobbyist_ID = ?"
  action_parameters = (salutation, lobbyist_id)
  rows_modified = datatier.perform_action(dbConn, update_sql, action_parameters)

  #return 1 if successful else 0
  if rows_modified > 0:
    return 1
  else:
    return 0