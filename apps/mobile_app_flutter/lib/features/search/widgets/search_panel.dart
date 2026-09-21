import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../navigation/providers/navigation_provider.dart';
import '../models/search_location.dart';
import '../providers/search_provider.dart';

enum SearchMode {
  none,
  source,
  destination,
}

class SearchPanel extends StatefulWidget {
  const SearchPanel({super.key});

  static final GlobalKey<_SearchPanelState> panelKey =
      GlobalKey<_SearchPanelState>();

  @override
  State<SearchPanel> createState() => _SearchPanelState();
}

class _SearchPanelState extends State<SearchPanel> {
  final TextEditingController destinationController =
      TextEditingController();

  SearchMode mode = SearchMode.none;

  @override
  void dispose() {
    destinationController.dispose();
    super.dispose();
  }

  void collapseSuggestions() {
    if (!mounted) return;

    setState(() {
      mode = SearchMode.none;
    });
  }

  Future<void> _refreshRoute(
    BuildContext context,
    SearchProvider provider,
  ) async {
    final nav =
        context.read<NavigationProvider>();

    final source =
        provider.selectedSource;

    final destination =
        provider.selectedDestination;

    if (destination == null) {
      return;
    }

    final sourceLat =
        source?.isCurrentLocation == true
            ? nav.sourceLat
            : source?.latitude ??
                nav.sourceLat;

    final sourceLon =
        source?.isCurrentLocation == true
            ? nav.sourceLon
            : source?.longitude ??
                nav.sourceLon;

    final destinationLat =
        destination.isCurrentLocation
            ? nav.sourceLat
            : destination.latitude;

    final destinationLon =
        destination.isCurrentLocation
            ? nav.sourceLon
            : destination.longitude;

    await nav.loadRoutes(
      sourceLat: sourceLat,
      sourceLon: sourceLon,
      destinationLat: destinationLat,
      destinationLon: destinationLon,
    );
  }

  @override
  Widget build(BuildContext context) {
    final provider =
        context.watch<SearchProvider>();

    final hasDestination =
        provider.selectedDestination != null;
    debugPrint(
      'SEARCH PANEL BUILDING '
      'SRC=${provider.selectedSource?.name} '
      'DEST=${provider.selectedDestination?.name}',
    );
    return Material(
      elevation: 8,
      color: Colors.white,
      borderRadius:
          BorderRadius.circular(20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (!hasDestination)
            InkWell(
              borderRadius:
                  BorderRadius.circular(20),
              onTap: () {
                setState(() {
                  mode =
                      SearchMode.destination;
                });
              },
              child: const Padding(
                padding:
                    EdgeInsets.all(16),
                child: Row(
                  children: [
                    Icon(Icons.search),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'Where are you going?',
                      ),
                    ),
                  ],
                ),
              ),
            ),

          if (hasDestination)
            Column(
              children: [
                InkWell(
                  onTap: () {
                    setState(() {
                      mode =
                          SearchMode.source;
                    });
                  },
                  child: Padding(
                    padding:
                        const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 14,
                    ),
                    child: Row(
                      children: [
                        const Icon(
                          Icons.my_location,
                          color:
                              Colors.green,
                        ),
                        const SizedBox(
                          width: 12,
                        ),
                        Expanded(
                          child: Text(
                            provider.selectedSource
                                    ?.name ??
                                'Current Location',
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                const Divider(height: 1),

                InkWell(
                  onTap: () {
                    setState(() {
                      mode =
                          SearchMode.destination;
                    });
                  },
                  child: Padding(
                    padding:
                        const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 14,
                    ),
                    child: Row(
                      children: [
                        const Icon(
                          Icons.search,
                        ),
                        const SizedBox(
                          width: 12,
                        ),
                        Expanded(
                          child: Text(
                            provider
                                    .selectedDestination
                                    ?.name ??
                                '',
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),

          if (mode != SearchMode.none)
            const Divider(height: 1),

          if (mode != SearchMode.none)
            SizedBox(
              height: 280,
              child: ListView(
                children: [
                  const _SectionHeader(
                    title: 'Favorites',
                  ),

                  if (provider
                      .favoritePlaces
                      .isEmpty)
                    const ListTile(
                      title: Text(
                        'No favorites yet',
                      ),
                    ),

                  ...provider.favoritePlaces.map(
                    (e) => _locationTile(
                      context,
                      provider,
                      e,
                      Icons.star,
                    ),
                  ),

                  if (provider
                      .recentSearches
                      .isNotEmpty) ...[
                    const _SectionHeader(
                      title:
                          'Recent Searches',
                    ),
                    ...provider.recentSearches.map(
                      (e) => _locationTile(
                        context,
                        provider,
                        e,
                        Icons.history,
                      ),
                    ),
                  ],

                  const _SectionHeader(
                    title: 'Popular Places',
                  ),

                  ...provider.popularPlaces.map(
                    (e) => _locationTile(
                      context,
                      provider,
                      e,
                      Icons.place,
                    ),
                  ),

                  if (provider
                      .filteredResults
                      .isNotEmpty) ...[
                    const _SectionHeader(
                      title: 'Results',
                    ),
                    ...provider.filteredResults.map(
                      (e) => _locationTile(
                        context,
                        provider,
                        e,
                        Icons.place,
                      ),
                    ),
                  ],
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _locationTile(
    BuildContext context,
    SearchProvider provider,
    SearchLocation location,
    IconData icon,
  ) {
    return ListTile(
      leading: Icon(icon),
      title: Text(location.name),
      onTap: () async {
        debugPrint(  
          'LOCATION TILE TAPPED: ${location.name}',
        );
        if (mode ==
            SearchMode.source) {
          provider.setSource(
            location,
          );
        } else {
          debugPrint(
            'SETTING DESTINATION',
          );
          await provider
              .setDestination(
            location,
          );
          debugPrint(
            'DEST NOW: ${provider.selectedDestination?.name}',
          );
        }

        await _refreshRoute(
          context,
          provider,
        );

        if (!mounted) return;

        setState(() {
          mode = SearchMode.none;
        });
      },
    );
  }
}

class _SectionHeader
    extends StatelessWidget {
  final String title;

  const _SectionHeader({
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding:
          const EdgeInsets.only(
        left: 16,
        top: 12,
        bottom: 6,
      ),
      child: Text(
        title,
        style: const TextStyle(
          fontWeight:
              FontWeight.bold,
        ),
      ),
    );
  }
}