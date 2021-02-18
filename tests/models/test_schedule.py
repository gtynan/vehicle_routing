from src.models.schedule import Schedule

class TestSchedule:

    def test_from_raw(self):
        driver_id = 1000
        route = [0, 1, 2, 0]
        distance_matrix = [[0, 10, 20], 
                           [10, 0, 30], 
                           [20, 30, 0]]
        schedule = Schedule.from_raw(driver_id, route, distance_matrix)
        
        assert schedule.driver.id == driver_id

        assert schedule.route[0].duration == 10
        assert schedule.route[0].start.name == "0"
        assert schedule.route[0].end.name == "1"

        assert schedule.route[1].duration == 30
        assert schedule.route[1].start.name == "1"
        assert schedule.route[1].end.name == "2"

        assert schedule.route[2].duration == 20
        assert schedule.route[2].start.name == "2"
        assert schedule.route[2].end.name == "0"