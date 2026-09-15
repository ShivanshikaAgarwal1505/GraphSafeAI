import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../providers/navigation_provider.dart';
import '../../widgets/route_summary_card.dart';
import '../../widgets/route_map_widget.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider =
        context.watch<NavigationProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'GraphSafeAI',
        ),
      ),

      body: Padding(
        padding:
            const EdgeInsets.all(16),

        child: provider.route == null
            ? Center(
                child: ElevatedButton(
                  onPressed:
                      provider.loading
                          ? null
                          : provider.loadRoute,

                  child: Text(
                    provider.loading
                        ? 'Loading...'
                        : 'Find Route',
                  ),
                ),
              )
            : Column(
                children: [

                  ElevatedButton(
                    onPressed:
                        provider.loading
                            ? null
                            : provider.loadRoute,

                    child: Text(
                      provider.loading
                          ? 'Loading...'
                          : 'Refresh Route',
                    ),
                  ),

                  const SizedBox(
                    height: 16,
                  ),

                  Expanded(
                    child:
                        SingleChildScrollView(
                      child: Column(
                        children: [

                          RouteSummaryCard(
                            route:
                                provider.route!,
                          ),

                          const SizedBox(
                            height: 16,
                          ),

                          const Text(
                            'MAP SHOULD APPEAR BELOW',
                            style: TextStyle(
                              fontSize: 20,
                              color:
                                  Colors.red,
                              fontWeight:
                                  FontWeight
                                      .bold,
                            ),
                          ),

                          const SizedBox(
                            height: 16,
                          ),

                          RouteMapWidget(
                            coordinates:
                                provider
                                    .route!
                                    .routeCoordinates,
                          ),

                          const SizedBox(
                            height: 30,
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
      ),
    );
  }
}