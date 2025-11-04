from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static

from wifi import NetworkManager
nm = NetworkManager()

net_list = nm.net_scan()
# print(nm.net_scan)


class LazyNM(App):

    def select_network(self, event) -> None:
        selected_wifi_text = event.control.text.split('(')[0]
        print(f"Selected Wi-Fi network: {selected_wifi_text}")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        self.sidebar = Vertical()
        self.wifi_list = Static()
        with Horizontal():
            # with Vertical(classes="side_bar"):
            #     yield Static('WiFi')
            #     yield Static('Device')
            with Vertical():
                for network in nm.net_scan():
                    wifi_item = Static(f"{network[7]} {network[1]} ({network[2]})")
                    wifi_item.add_class("wifi_item")
                    # wifi_item.on_click(self.select_network)
                    yield wifi_item

    def on_mount(self) -> None:
        wifi_list_style = self.wifi_list.styles
        # wifi_list_style.background = 'green'
        wifi_list_style.border = ("heavy", "green")

if __name__ == "__main__":
    ...
