from datetime import datetime
from typing import Optional

try:
    from rich.align import Align
    from rich.console import Console, Group
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress_bar import ProgressBar
    from rich.table import Table
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False


from .context import Context


class TelemetryTUI:
    """
    F1 Pit Wall Telemetry style TUI using `rich`.
    Renders live stream of network requests at the top, and real-time telemetry metrics at the bottom.
    """

    def __init__(self, context: Context):
        self.context = context
        self.start_time = datetime.now()
        self._live: Optional[Live] = None
        self._console = Console() if HAS_RICH else None

    def start(self):
        if not HAS_RICH:
            return
        self._live = Live(
            self._generate_layout(),
            console=self._console,
            refresh_per_second=4,
            screen=True,
            auto_refresh=True,
            redirect_stdout=True,
            redirect_stderr=True,
        )
        self._live.start()

    def stop(self):
        if self._live:
            self._live.stop()
            self._live = None

    def update(self):
        if self._live and self._live.is_started:
            self._live.update(self._generate_layout())

    def _generate_layout(self) -> Layout:
        layout = Layout()
        layout.split(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="telemetry", size=10),
        )

        layout["header"].update(self._make_header())
        layout["body"].update(self._make_stream_panel())
        layout["telemetry"].update(self._make_telemetry_panel())

        return layout

    def _make_header(self) -> Panel:
        elapsed = datetime.now() - self.start_time
        hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        title = Text()
        title.append(" 🏎️  COMPRESSION PROXY ", style="bold italic yellow")
        title.append(" // ", style="dim white")
        title.append("LIVE TELEMETRY DASHBOARD", style="bold cyan")

        subtext = Text()
        subtext.append(f"SESSION: {timer_str} ", style="bold white")
        subtext.append("│ ", style="dim grey")
        subtext.append("STATUS: ", style="dim white")
        subtext.append("🟢 LIVE TELEMETRY ", style="bold green")

        header_table = Table.grid(expand=True)

        header_table.add_column(justify="left")
        header_table.add_column(justify="right")
        header_table.add_row(title, subtext)

        return Panel(
            header_table,
            style="on #121212",
            border_style="bright_blue",
            subtitle="[bold dim grey]SYS.v0.1.0[/bold dim grey]",
            subtitle_align="right",
        )

    def _make_stream_panel(self) -> Panel:
        table = Table(
            expand=True,
            box=None,
            header_style="bold bright_cyan on #1e1e2e",
            border_style="dim white",
            pad_edge=False,
        )
        table.add_column("TIME", style="dim cyan", width=10)
        table.add_column("FLOW / ENDPOINT", style="bold white", ratio=4)
        table.add_column("TYPE", style="yellow", ratio=2)
        table.add_column("BEFORE", style="dim white", justify="right", ratio=1)
        table.add_column("AFTER", style="bold green", justify="right", ratio=1)
        table.add_column("SAVED", style="bold magenta", justify="right", ratio=1)
        table.add_column("STATUS", justify="center", ratio=1)

        flows = self.context.get_recent_flows()
        now_str = datetime.now().strftime("%H:%M:%S")

        if not flows:
            table.add_row(
                now_str,
                "Awaiting network traffic...",
                "-",
                "-",
                "-",
                "-",
                "[dim]STANDBY[/dim]",
            )
        else:
            for item in flows[:15]:
                before_str = self._format_bytes(item["before"])
                after_str = self._format_bytes(item["after"])
                savings_str = f"{item['savings']}%" if item["savings"] > 0 else "-"

                status_style = "bold green"
                if item["status"] == "BLOCKED":
                    status_style = "bold red"
                    before_str = "-"
                    after_str = "-"
                    savings_str = "100%"
                elif item["status"] == "PASSTHROUGH":
                    status_style = "dim white"

                status_badge = f"[{status_style}]{item['status']}[/{status_style}]"

                url = item["url"]
                if len(url) > 65:
                    url = url[:32] + "..." + url[-30:]

                table.add_row(
                    now_str,
                    url,
                    item["type"][:20],
                    before_str,
                    after_str,
                    savings_str,
                    status_badge,
                )

        return Panel(
            table,
            title="[bold cyan]⚡ LIVE REQUEST STREAM[/bold cyan]",
            title_align="left",
            border_style="cyan",
            style="on #0d0e15",
        )

    def _make_telemetry_panel(self) -> Panel:
        stats = self.context.get_stats()

        # Box 1: Compression Gauge
        before_mb = stats["before_bytes"] / (1024 * 1024)
        after_mb = stats["after_bytes"] / (1024 * 1024)
        saved_mb = stats["saved_bytes"] / (1024 * 1024)
        savings_pct = stats["savings_pct"]

        pbar = ProgressBar(
            total=100,
            completed=min(100, max(0, savings_pct)),
            width=25,
            style="red on #222222",
            complete_style="bright_green",
            finished_style="bright_green",
        )

        comp_text = Text()
        comp_text.append(f"BEFORE : {before_mb:8.3f} MB\n", style="bold white")
        comp_text.append(f"AFTER  : {after_mb:8.3f} MB\n", style="bold green")
        comp_text.append(f"SAVED  : {saved_mb:8.3f} MB ", style="bold magenta")
        comp_text.append(f"({savings_pct}%)\n", style="bold yellow")

        comp_group = Group(comp_text, Align.center(pbar))

        panel_comp = Panel(
            comp_group,
            title="[bold green]⚡ COMPRESSION RATIO[/bold green]",
            border_style="green",
            style="on #0a150f",
        )

        # Box 2: Ads & Trackers Interception
        ads_text = Text()
        ads_text.append("\n  INTERCEPTED  \n", style="dim white")
        ads_text.append(f"  🛡️ {stats['ads_blocked']}  \n", style="bold red blink")
        ads_text.append("  ADS & TRACKERS  \n", style="bold yellow")

        panel_ads = Panel(
            Align.center(ads_text),
            title="[bold red]🛡️ AD & TRACKER SHIELD[/bold red]",
            border_style="red",
            style="on #1c0a0a",
        )

        # Box 3: Flow Metrics
        tot_req = stats["total_requests"]
        comp_req = stats["compressed_requests"]
        eff_pct = round((comp_req / tot_req) * 100, 1) if tot_req > 0 else 0.0

        flow_text = Text()
        flow_text.append(f"TOTAL FLOWS : {tot_req}\n", style="bold cyan")
        flow_text.append(f"COMPRESSED  : {comp_req}\n", style="bold green")
        flow_text.append(f"EFFICIENCY  : {eff_pct}%\n", style="bold yellow")
        flow_text.append("LOG FILE    : ACTIVE", style="dim white")

        panel_flow = Panel(
            flow_text,
            title="[bold yellow]📊 DATA VOLUME TELEMETRY[/bold yellow]",
            border_style="yellow",
            style="on #1a1600",
        )

        # Combine inside grid
        grid = Table.grid(expand=True)
        grid.add_column(ratio=2)
        grid.add_column(ratio=1)
        grid.add_column(ratio=2)
        grid.add_row(panel_comp, panel_ads, panel_flow)

        return Panel(
            grid,
            title="[bold white on blue] 🏎️ LIVE CONTEXT TELEMETRY (BOTTOM) [/bold white on blue]",
            title_align="center",
            border_style="bright_blue",
            style="on #08090f",
        )

    def _format_bytes(self, num_bytes: float) -> str:
        if num_bytes <= 0:
            return "0 B"
        if num_bytes < 1024:
            return f"{int(num_bytes)} B"
        elif num_bytes < 1024 * 1024:
            return f"{num_bytes / 1024:.1f} KB"
        else:
            return f"{num_bytes / (1024 * 1024):.2f} MB"
