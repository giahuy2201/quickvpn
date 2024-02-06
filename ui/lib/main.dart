import 'dart:convert';

import 'package:country_flags/country_flags.dart';
import 'package:flutter/material.dart';
import 'package:ui/models/instance.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const QuickVPNApp());
}

class QuickVPNApp extends StatelessWidget {
  const QuickVPNApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'QuickVPN',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomePage(title: 'QuickVPN'),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.title});
  final String title;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late Future<List<Instance>> futureInstances;

  @override
  void initState() {
    super.initState();
    futureInstances = fetchInstances();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: FutureBuilder<List<Instance>>(
        future: futureInstances,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            return ListView.builder(
              shrinkWrap: true,
              itemCount: snapshot.data!.length,
              itemBuilder: (context, index) {
                return ListTile(
                  leading: CircleAvatar(
                    backgroundColor: Colors.transparent,
                    child: CountryFlag.fromCountryCode(
                      snapshot.data![index].country.toString(),
                    ),
                  ),
                  title: Text(snapshot.data![index].label.toString()),
                  trailing: Text(snapshot.data![index].expiration.toString()),
                  subtitle: Text(snapshot.data![index].ipv4.toString()),
                );
              },
            );
          } else if (snapshot.hasError) {
            return Text('${snapshot.error}');
          }

          // By default, show a loading spinner.
          return const CircularProgressIndicator();
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: null,
        tooltip: 'Add new instance',
        child: const Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

Future<List<Instance>> fetchInstances() async {
  final response =
      await http.get(Uri.parse('http://127.0.0.1:8000/api/instances'));

  if (response.statusCode == 200) {
    final List result = json.decode(response.body);
    return result.map((e) => Instance.fromJson(e)).toList();
  } else {
    throw Exception('Failed to load instances');
  }
}
