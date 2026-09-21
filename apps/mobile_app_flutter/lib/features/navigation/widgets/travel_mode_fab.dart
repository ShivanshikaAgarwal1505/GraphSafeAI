import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/travel_mode.dart';
import '../providers/navigation_provider.dart';
import '../../search/providers/search_provider.dart';

class TravelModeFab
    extends StatelessWidget {
  const TravelModeFab({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final nav =
        context.watch<NavigationProvider>();

    final search =
        context.read<SearchProvider>();

    return FloatingActionButton(
      heroTag: 'travel_mode',

      onPressed: () async {
        final destination =
            search.selectedDestination;

        if (destination == null) {
          return;
        }

        await nav.toggleTravelMode(
          destinationLat:
              destination.latitude,
          destinationLon:
              destination.longitude,
        );
      },

      child: Icon(
        nav.selectedTravelMode ==
                TravelMode.walking
            ? Icons.directions_walk
            : Icons.directions_car,
      ),
    );
  }
}