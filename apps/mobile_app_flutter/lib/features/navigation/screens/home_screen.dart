import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../location/providers/location_provider.dart';
import '../providers/navigation_provider.dart';

import '../../search/widgets/search_panel.dart';

import '../widgets/bottom_metrics_card.dart';
import '../widgets/route_map_widget.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({
    super.key,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
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
    });
  }

  @override
  Widget build(BuildContext context) {
    final provider =
        context.watch<NavigationProvider>();

    return Scaffold(
      body: Stack(
        children: [
          Positioned.fill(
            child: RouteMapWidget(
              coordinates:
                  provider.route?.routeCoordinates ?? [],
              centerLat: provider.sourceLat,
              centerLon: provider.sourceLon,
            ),
          ),

          const Positioned(
            top: 50,
            left: 16,
            right: 16,
            child: SearchPanel(),
          ),

          if (provider.route != null)
            Positioned(
              left: 16,
              right: 16,
              bottom: 20,
              child: BottomMetricsCard(
                route: provider.route!,
              ),
            ),
        ],
      ),
    );
  }
}