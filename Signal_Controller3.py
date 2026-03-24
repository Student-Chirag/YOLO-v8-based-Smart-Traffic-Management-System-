
import time

class TrafficSignalController:
    def __init__(self):
        self.base_green_time = 15        # minimum green time (sec)
        self.time_per_vehicle = 0.4      # time per vehicle (sec)
        self.yellow_time = 4             # yellow signal time (sec)
        self.max_green_time = 80
        self.min_green_time = 15

    def calculate_green_time(self, vehicle_count):
        if vehicle_count == 0:
            return self.min_green_time

        green_time = self.base_green_time + (vehicle_count * self.time_per_vehicle)
        green_time = max(self.min_green_time,
                         min(green_time, self.max_green_time))
        return round(green_time)

    def run_one_cycle(self, traffic_data):
        print("\n🔁 New Traffic Cycle Started")

        # Sort lanes by traffic density (priority)
        sorted_lanes = sorted(
            traffic_data.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Pre-calculate green times
        green_times = {}
        for lane, count in sorted_lanes:
            green_times[lane] = self.calculate_green_time(count)

        # Total cycle time (green + yellow for all lanes)
        total_cycle_time = sum(
            green_times[lane] + self.yellow_time for lane in green_times
        )

        # Run signal for each lane
        for lane, count in sorted_lanes:
            green_time = green_times[lane]

            # Red time = total cycle time - (own green + yellow)
            red_time = total_cycle_time - (green_time + self.yellow_time)

            print("\n--------------------------------")
            print(f"{lane} → GREEN for {green_time} seconds")
            print(f"{lane} → YELLOW for {self.yellow_time} seconds")
            print(f"{lane} → RED for {red_time} seconds")
            print(f"Vehicle Count : {count}")
            print("--------------------------------")
            time.sleep(2)  # simulation delay

def main():
    traffic_data = {
        "Lane A": int(input("Enter vehicle count in Lane A: ")),
        "Lane B": int(input("Enter vehicle count in Lane B: ")),
        "Lane C": int(input("Enter vehicle count in Lane C: ")),
        "Lane D": int(input("Enter vehicle count in Lane D: "))
    }

    controller = TrafficSignalController()
    controller.run_one_cycle(traffic_data)

    print("\n🔄 Traffic density will be re-evaluated in the next cycle.")

if __name__ == "__main__":
    main()
