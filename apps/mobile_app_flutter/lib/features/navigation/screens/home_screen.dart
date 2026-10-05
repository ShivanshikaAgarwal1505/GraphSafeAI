import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../location/providers/location_provider.dart';
import '../providers/navigation_provider.dart';

import '../../search/widgets/search_panel.dart';
import '../../search/providers/search_provider.dart';

// import '../widgets/bottom_metrics_card.dart';
import '../widgets/route_map_widget.dart';
import '../widgets/travel_mode_fab.dart';
import '../widgets/route_selector_chips.dart';

import '../../reports/widgets/quick_report_sheet.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({
    super.key,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final searching =
    SearchPanel.panelKey.currentState
            ?.isOpen ??
        false;

  @override
  void initState() {
    super.initState();

    WidgetsBinding.instance.addPostFrameCallback((_) async {
      final locationProvider =
          context.read<LocationProvider>();

      await locationProvider.loadLocation();

      if (!mounted) return;

      final position = locationProvider.position;
      
      if (position != null) {
        context.read<NavigationProvider>().setCurrentLocation(
              latitude: position.latitude,
              longitude: position.longitude,
            );
      }

      await context
        .read<SearchProvider>()
        .initialize();
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider =
      context.watch<NavigationProvider>();

    return Scaffold(

      body: Listener(
        behavior: HitTestBehavior.translucent,
        
        onPointerDown: (_) {
          FocusManager.instance.primaryFocus?.unfocus();
          // SearchPanel.panelKey.currentState?.collapseSuggestions();
        },
        child: Stack(
          children: [
            Positioned.fill(
              child: RouteMapWidget(
                safeRoute: provider.safeRoute,
                balancedRoute: provider.balancedRoute,
                fastestRoute: provider.fastestRoute,
                selectedRoute: provider.selectedRoute,
                centerLat: provider.sourceLat,centerLon: provider.sourceLon,
              ),
            ),

            Positioned(
              top: 16,
              left: 16,
              right: 16,
              child: SearchPanel(key: SearchPanel.panelKey,),
            ),

            Positioned(
              right: 20,
              bottom: 20,
              child: TravelModeFab(),
            ),

            if (
              provider.activeRoute != null &&
              !searching
            )
            Positioned(
              top: 150,
              right: 12,
              child: const RouteSelectorChips(),
            ),

            Positioned(
              left: 20,
              bottom: 20,
              child: FloatingActionButton(
                heroTag: "quick_report",
                backgroundColor: Colors.red,
                foregroundColor: Colors.white,
                onPressed: () {
                  showModalBottomSheet(
                  context: context,
                  isScrollControlled: true,
                  builder: (_) => const QuickReportSheet(),
                  );
                  },
                child: const Icon(
                  Icons.warning_amber,
                ),
                
              ),
            ),
          ],
        ),
      ),
    );
  }
}