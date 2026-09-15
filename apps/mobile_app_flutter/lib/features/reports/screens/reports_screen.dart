import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../models/report_request.dart';

import '../../location/providers/location_provider.dart';

import '../providers/reports_provider.dart';

class ReportsScreen extends StatefulWidget {
  const ReportsScreen({
    super.key,
  });

  @override
  State<ReportsScreen> createState() =>
      _ReportsScreenState();
}

class _ReportsScreenState
    extends State<ReportsScreen> {
  String category = 'HARASSMENT';

  int severity = 3;

  final TextEditingController
      descriptionController =
      TextEditingController();

  @override
  Widget build(BuildContext context) {
    final provider =
        context.watch<ReportsProvider>();

    final locationProvider =
        context.watch<LocationProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Reports',
        ),
      ),

      body: SingleChildScrollView(
        padding:
            const EdgeInsets.all(16),

        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,

          children: [

            FilledButton.icon(
              onPressed: () async {
                await locationProvider
                    .loadLocation();
              },

              icon: const Icon(
                Icons.my_location,
              ),

              label: const Text(
                'Use Current Location',
              ),
            ),

            const SizedBox(
              height: 16,
            ),

            Card(
              child: Padding(
                padding:
                    const EdgeInsets.all(
                        12),

                child: Column(
                  crossAxisAlignment:
                      CrossAxisAlignment
                          .start,

                  children: [

                    const Text(
                      'Selected Location',
                      style: TextStyle(
                        fontWeight:
                            FontWeight.bold,
                      ),
                    ),

                    const SizedBox(
                      height: 8,
                    ),

                    Text(
                      'Latitude: ${locationProvider.position?.latitude ?? "Not Selected"}',
                    ),

                    Text(
                      'Longitude: ${locationProvider.position?.longitude ?? "Not Selected"}',
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(
              height: 20,
            ),

            const Text(
              'Category',
            ),

            DropdownButton<String>(
              isExpanded: true,

              value: category,

              items: const [

                DropdownMenuItem(
                  value: 'HARASSMENT',
                  child: Text(
                    'Harassment',
                  ),
                ),

                DropdownMenuItem(
                  value: 'THEFT',
                  child: Text(
                    'Theft',
                  ),
                ),

                DropdownMenuItem(
                  value: 'ASSAULT',
                  child: Text(
                    'Assault',
                  ),
                ),

                DropdownMenuItem(
                  value: 'VANDALISM',
                  child: Text(
                    'Vandalism',
                  ),
                ),
              ],

              onChanged: (value) {
                if (value == null){
                  return;
                }

                setState(() {
                  category = value;
                });
              },
            ),

            const SizedBox(
              height: 20,
            ),

            Text(
              'Severity: $severity',
            ),

            Slider(
              value:
                  severity.toDouble(),

              min: 1,

              max: 5,

              divisions: 4,

              onChanged: (value) {
                setState(() {
                  severity =
                      value.toInt();
                });
              },
            ),

            const SizedBox(
              height: 20,
            ),

            TextField(
              controller:
                  descriptionController,

              maxLines: 4,

              decoration:
                  const InputDecoration(
                labelText:
                    'Description',

                border:
                    OutlineInputBorder(),
              ),
            ),

            const SizedBox(
              height: 20,
            ),

            FilledButton(
              onPressed:
                  provider.loading
                      ? null
                      : () async {

                          final latitude =
                              locationProvider
                                      .position
                                      ?.latitude ??
                                  0;

                          final longitude =
                              locationProvider
                                      .position
                                      ?.longitude ??
                                  0;

                          final request =
                              ReportRequest(
                            latitude:
                                latitude,

                            longitude:
                                longitude,

                            category:
                                category,

                            severity:
                                severity,

                            description:
                                descriptionController
                                    .text,

                            source:
                                'CITIZEN',

                            timestamp:
                                DateTime.now(),
                          );

                          final messenger = ScaffoldMessenger.of(context);
                          
                          await provider
                              .submitReport(
                            request,
                          );

                          if (!mounted) {
                            return;
                          }
                          

                          final responseMessage =
                            provider.response?.message ??
                            'Submitted';

                          messenger.showSnackBar(

                            SnackBar(
                              content: Text(
                                responseMessage,
                              ),
                            ),
                          );
                        },

              child: Text(
                provider.loading
                    ? 'Submitting...'
                    : 'Submit Report',
              ),
            ),

            const SizedBox(
              height: 20,
            ),

            if (provider.response !=
                null)

              Card(
                child: Padding(
                  padding:
                      const EdgeInsets
                          .all(12),

                  child: Text(
                    'Report ID: ${provider.response!.id}',
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}