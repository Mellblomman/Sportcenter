import pytest
from unittest.mock import patch
from app import delete_booking_from_database
from app import register_user_status
from app import app


#Kör en test för att se så den kan plocka bort bokningar
@patch('app.psycopg2.connect')
def test_delete_booking_from_database(mock_connect):
    booking_id = 123
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.rowcount = 1
    assert delete_booking_from_database(booking_id) == True
    mock_cursor.execute.assert_called_once_with("DELETE FROM bookinginformation WHERE booking_id = %s", (booking_id,))
    mock_connect.return_value.commit.assert_called_once()
    mock_cursor.rowcount = 0
    assert delete_booking_from_database(booking_id) == False

