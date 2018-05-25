# Test Plan for Imsi Investigation Web Application

This page contains the test cases used to test the Imsi Web Tracker Application.

| Test description                                               | Outcome Expected                                    |
|----------------------------------------------------------------|-----------------------------------------------------|
| **IMSI** and **email** tracking files don't exist| <ol><li>Initial page should load with the list areas for the email and imsi list should show message indicating nothing added yet.</li><li>Add only Imsi(s) should update displayed Imsi list and email should still indicate no emails added yet.</li><li>Add an email to the list which should add the file and update email list display portion with new entry</li></ol> |
| <ul><li>Add single IMSI with and without alias</li><li>Add multiple IMSIS(S) at once using defined format with and without alias.</li><li>Add just an email address.</li><li>Add both an Imsi and an email address in one submission.</li></ul> | Display should show newly added Imsis and/or email address |
| Try to add an Imsi that is already in the list, either with or without the alias | "IMSI(s) successfully added" message displays but a duplicate IMSI should not show up in the list.|
| Try to add or delete an email that is not a valid email address (i.e. doesn't include an @ in the value) | Error message should be displayed indicating email entered is not valid. |
| Delete an Imsi or a list of Imsis using the approved format | Successful delete message displayed and Imsi(s) deleted should not show up on the display
| Delete an Email | Successful delete message displayed and email should not show up on the display |
| Filter the Imsi List by an Imsi and alias | List of Imsis should only contain items that match the search string.