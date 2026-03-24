import time

class TrafficSignalController:
    def __init__(self):
        self.base_green_time = 15        # minimum green time (sec)
        self.time_per_vehicle = 0.4      # time per vehicle (sec)
        self.yellow_time = 4             # yellow signal time (sec)
        self.max_green_time = 80
        self.min_green_time = 15         # even if no vehicles

    def calculate_green_time(self, vehicle_count):
        if vehicle_count == 0:
            return self.min_green_time

        green_time = self.base_green_time + (vehicle_count * self.time_per_vehicle)
        green_time = max(self.min_green_time,
                         min(green_time, self.max_green_time))
        return round(green_time)

    def run_one_cycle(self, traffic_data):
        print("\n🔁 New Traffic Cycle Started")

        # Priority: highest vehicle count first
        sorted_lanes = sorted(
            traffic_data.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for lane, count in sorted_lanes:
            green_time = self.calculate_green_time(count)

            print("\n--------------------------------")
            print(f"{lane} → GREEN")
            print(f"Vehicle Count : {count}")
            print(f"Green Time    : {green_time} seconds")
            print("Other Lanes   : RED")
            time.sleep(2)  # simulation (use green_time in real system)
            print(f"{lane} → YELLOW for {self.yellow_time} seconds")
            time.sleep(1)
            # print(f"{lane} → RED for {red_time} seconds")
            print(f"{lane} → RED")

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


