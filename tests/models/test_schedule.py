from src.models.schedule import Schedule
from datetime import datetime, timedelta, date


class TestSchedule:
    def test_from_raw(self):
        driver_id = 1000
        route = [0, 1, 2, 0]
        time = [0, 10, 20, 30]
        schedule = Schedule.from_raw(driver_id, route, time)

        assert schedule.driver.id == driver_id

        assert schedule.route[0].duration == 10
        assert schedule.route[0].start.name == "0"
        assert schedule.route[0].end.name == "1"

        assert schedule.route[1].duration == 10
        assert schedule.route[1].start.name == "1"
        assert schedule.route[1].end.name == "2"

        assert schedule.route[2].duration == 10
        assert schedule.route[2].start.name == "2"
        assert schedule.route[2].end.name == "0"

        # comparing final arrival time with expected
        expected_date = datetime.now() + timedelta(seconds=time[-1])
        actual_date = datetime.combine(date.today(), schedule.route[-1].arrival_time)
        assert abs(expected_date - actual_date < timedelta(seconds=2))
