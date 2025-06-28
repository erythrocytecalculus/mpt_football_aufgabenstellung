# Machine Perception and Tracking - Semesteraufgabe
## Modus Operandi
Sie bilden Teams mit maximal 4 Personen und entwickeln mit Hilfe der Techniken aus der Vorlesung
einen eigenen Algorithmus um Fußballspiele zu analysieren. Sie stellen ihre Ergebnisse am Ende der Vorlesung vor (Termine werden noch festgelegt). Ihr Team hat für diese Vorstellung 30 Minuten Zeit. In dieser Zeit müssen Sie ihren Code vorführen und im Detail vorstellen. Jedes Teammitglied muß seinen eigenen, individuellen Beitrag zum Projekt konkret bennenen können und auch entsprechende, dazu passende Commits im GIT-Repository vorzeigen können. Unabhängig davon sind Sie aber ein Team und arbeiten gemeinsam an dem gesamten Projekt. Wenn Sie sich z.B. aufteilen und verschiedene Teile bearbeiten müssen Sie trotzdem sicherstellen das am Ende alles zusammen funktioniert. Ihre Prüfungsaufgabe besteht darin ein vollständig funktionsfähiges Repository abzugeben, unabhängig davon wer welche Teile bearbeitet hat. Helfen Sie ihren Teamkollegen und springen Sie für diese ein falls nötig.

Um es noch einmal ganz klar zu sagen: Es ist nicht ausreichend nur einen Teil der Module zu bearbieten (z.B. nur den Shirt Classifier) und dann auf die fehlenden Beiträge der Teamkollegen zu verweisen.

Sie können (und sollten) während des gesamten Semesters an diesem Projekt arbeiten. Schieben Sie die Arbeit nicht in die letzten Wochen, dafür ist die Komplexität und auch der Abstimmungsbedarf zu groß. Während der Praktikum (Montags, 09:00 Uhr bis 11:00 Uhr im ZDD KI Labor) haben Sie die Möglichkeit, Fragen zu stellen, über ihren Projektfortschritt zu berichten oder Probleme gemeinsam mit dem Dozenten zu lösen. Nutzen Sie diese Zeit während dem Semester da auch ich am Ende des Semesters traditionell mit anderen wichtigen Aufgaben beschäftigt sein werde.

Zusätzlich zu dieser praktischen Projektaufgabe müssen Sie drei Semesterbegleitende Quizze in Moodle bearbeiten. Diese werden zu gegebener Zeit freigeschaltet und sind dann für zwei Wochen bearbeitbar.

## Bewertungskriterien und Punktevergabe
Die praktische Projektabgabe macht 80% der Gesamtnote aus. Achten Sie darauf das ihr Code vollständig ist und ohne weitere Einschränkungen lauffähig ist. Wenn Sie Python-Module verwenden stellen sie z.B. eine entsprechende requirements.txt Datei bereit um diese zu installieren. Darüberhinaus Linten sie ihren Code mit [BLACK](https://github.com/psf/black)!

Bewertungskriterien für den Code sind Funktionalität, Effizienz und ob die aus der Vorlesung vorgestellten Techniken korrekt angewendet wurden. In ihrem mündlichen Abschlußvortrag sollten Sie auf diese Punkte eingehen, insbesondere sollten Sie die von Ihnen verwendeten Techniken konkret bennenen und deren jeweilige Wahl motivieren können.

Die drei semesterbegleitenden Moodlequizze machen darüber hinaus jeweils 10% der Gesamtnote aus. Bearbeiten Sie die Moodle Quizze sobald diese freigeschaltet werden und geben sie sie rechtzeig ab damit ihre erreichte Punktzahl berücksichtigt werden kann.

## Projektvorstellung
Die Teams präsentieren ihre Ergebnisse in einem 30 minütigen Vortrag mit anschließendem Frageteil (etwa 15 Minuten). Bereiten Sie dazu eine entsprechende Folienpräsentation vor die sie ebenfalls als Teil ihres Repositories mit abgeben (einchecken!). Präsentieren Sie auf jedenfall das funktionsfähige Repository (also alle vier Module) auf einer Auswahl von Videos. Gehen Sie dann auf Details der Implementierung ein und bennenen Sie ihren jeweiligen, individuellen Beitrag. Zeigen Sie ihre Implementierung im Code sowie die dazugehörigen Git-Commits. Sie sollten in der Lage sein Fragen zu ihrem Code zu beantworten.


## Bereitgestellte Infrastruktur
Im Rahmen dieses Projektes erhalten Sie eine umfassende Infrastruktur von der HSD damit Sie sich auf die wesentliche Lernziele konzentrieren können. Insbesondere erhalten Sie mit diesem Code-Repository eine vollständige Re-Simulations Umgebung sowie 20 Videos inklusive Daten. Die Re-Simulation ist in der Lage die zwischen den verschiedenen Modulen ausgetauschten Daten zu serialisieren und auf der Festplatte abzuspeichern. Umgekehrt kann die Re-Simulationsumgebung auch einmal gespeicherte Daten von der Festplatte einlesen und wieder abspielen, so als ob diese vom jeweiligen Modul live berechnet worden wären. In Vorbereitung auf diese Veranstaltung habe ich für alle bereitgestellten Videos bereits einmal Daten aus meiner Musterlösung für sie serialisiert und ebenfalls bereitgestellt. Das erlaubt Ihnen unabhängig von ihren Team-Mitgliedern an allen Modules des Projektes gleichzeitig zu arbeiten. So können sie z.B. am s.g. Shirt Classifier arbeiten und dazu die wieder eingespielten Informationen des Trackers verwenden ohne diesen bereits vorher implementiert haben zu müssen. Sobald ihr eigener Tracker dann fertig ist können Sie diesen einfach gegen die vorher aufgezeichneten Daten austauschen und so Stück für Stück ihren gesamten Algorithmus aufbauen.

In der Datei main.py finden Sie die Definition der Re-Simulationsumgebung inklusive aller Module und der zwischen den Modulen ausgetauschten Signalen. Insbesondere finden Sie die Definition der Engine Klasse

    engine = Engine(
      modules=[
        VideoReader(targetSize=shape),
        recordReplayMultiplex(Detector(), RRPlexMode.REPLAY),
        recordReplayMultiplex(OpticalFlow(), RRPlexMode.REPLAY),
        recordReplayMultiplex(Tracker(), RRPlexMode.REPLAY),
        recordReplayMultiplex(ShirtClassifier(), RRPlexMode.REPLAY),
        Display(historyBufferSize=1000)
        ],
      signals={
        ...
      })

Hier werden die von Ihnen in diesem Projekt zu implementierenden Module "Detector", "OpticalFlow", "Tracker" und "ShirtClassifier" instanziert. Gleichzeit werden die Module mit der Methode "recordReplayMultiplex" gewrappt. An dieser Stelle können Sie über den zweite Parameter steuern, wie das Modul sich verhalten soll. Dabei verwenden Sie einen der drei folgenden Modi:

    class RRPlexMode(Enum):
      BYPASS = 1
      RECORD = 2
      REPLAY = 3

Mittels RRPlexMode.BYPASS ignorieren Sie den Recording und Replay Mechanismus und verwenden stattdessen die Ergebnisse ihres eigenen Moduls. Am Ende ihre Projektes müssen alle vier Module in diesem Modus gefahren werden. Solange in Module jedoch noch nicht fertig ist können Sie mittels RRPlexMode.REPLAY auch vorher aufgezeichnete Ergebnisse von der Festplatte laden und abspielen. Laden Sie am Anfang des Semesters die von mir bereits simulierten Ergebnisse herunter damit Sie diesen Modus nutzen können. In diesem Modus können Sie bereits an nachgelagerten Modulen (z.B. dem Tracker) arbeiten ohne das sie bereits einen sinnvollen, eigenen Detektor implementiert haben. Dies erlaubt Ihnen parallel mit ihren Teamkollegen zu arbeiten ohne auf deren Ergebnisse warten zu müssen.

Theoretisch können Sie auch den RRPlexMode.RECORD Moduus verwenden. In diesem Fall würden Sie die Ergebnisse ihres Moduls auf die Festplatte schreiben um diese später wiederverwenden zu können. Beachten Sie dabei jedoch das sie meine Ergebnisse überschreiben würden. Sollte ihnen dies aus Versehen passieren können Sie natürlich jederzeit erneut die Original-Daten herunterladen.

## Wo finde ich die Daten
Laden Sie die 20 Beispielvideos sowie die aufgezeichneten Resimulationsdaten hier herunter:

https://drive.google.com/drive/folders/1YYTo94fbUk4Tsny36_v9eUMrU6BHoQ9N?usp=sharing

## Die vier Module
In diesem Projekt müssen Sie vier Module implementieren und die jeweils benötigten Signale korrekt an die nachfolgenden Module weiterleiten. Jedes Modul implementiert dabei eine Klasse mit der folgenden API:

    class Module():
      def __init__(self):
        pass

      def start(self, data):
        pass

      def step(self, data):
        pass

      def stop(self, data):
        pass

Dabei wird die start Methode genau einmal am Anfang der Verarbeitungskette aufgerufen, die Stop Methode genau einmal am Ende. Jenachdem wie sie ihr Modul implementieren kann es sein das sie diese beiden Methoden gar nicht benötigen, in diesem Fall können sie die Methoden leer lassen.

Wichtig ist vor allem das sie die step(...) Methode korrekt implementieren. Diese Methode wird von der Re-Simulationsumgebung einmal für jeder neue Videobild aufgerufen. Über den "data" Parameter erhalten Sie alle Signale der vorangegangenen Module, insbesondere so zum Beispiel das vom VideoReader Modul eingelesene Kamerabild oder die Detektionen, die der Detektor zur Verfügung stellt.

Sie müssen in der Step-Methode ihre Ergebnisse berechnen und diese als Rückgabewert in Form eines Python-Dictionaries zurückgeben. Dabei müssen sie die Signale korrekt bennen und auch die erwarteten Datentypen korrekt einhalten. Ich habe bereits eine Visualisierung aller Signale implementiert so dass Sie sich darum nicht kümmern müssen. Damit die Darstellung korrekt funktioniert ist jedoch erforderlich, dass Sie sich genau an die Definitionen im Skript halten. Die Re-Simulationsumgebung validiert ihre Rückgaben und bricht die Verarbeitung mit einer hilfreichen Fehlermeldung ab falls Sie Signale nicht oder falsch befüllen.

## Detektor
Die Aufgabe des Detektors besteht darin, den Ball, die Torhüter, die Spieler und die Schiedsrichter zu erkennen, falls sie sichtbar sind.
Für jedes erkannte Objekt muss eine Begrenzungsbox (Bounding Box) definiert werden, die die zentrale Position des Objekts (X, Y) sowie dessen Breite und Höhe (W, H) umfasst.
Es kann eine beliebige Anzahl von Objekten zurückgegeben werden.

Hinweis: Sie können auf data["image"] zugreifen, um das aktuelle Bild zu erhalten.
Rückgabe eines Wörterbuchs mit den Erkennungen und den zugehörigen Klassen.

Die Detektionen müssen ein Nx4-NumPy-Tensor sein, wobei jedes erkannte Objekt durch einen vierdimensionalen Vektor dargestellt wird.
Der Erkennungstensor ist im Format (X, Y, W, H) codiert, wobei X- und Y-Koordinaten zuerst kommen, gefolgt von Breite (W) und Höhe (H) der jeweiligen Begrenzungsbox.
Die X- und Y-Koordinaten stellen den Mittelpunkt des Objekts dar. Daher wird die Begrenzungsbox von (X - W/2, Y - H/2) bis (X + W/2, Y + H/2) gezeichnet.
Die Klassen müssen ein Nx1-NumPy-Tensor sein, mit jeweils einem skalaren Eintrag pro Erkennung.
Für jede erkannte Instanz muss folgende Zuordnung verwendet werden:

    0: Ball
    1: Torhüter
    2: Spieler
    3: Schiedsrichter

Ihre Rückgabe sieht so aus

    return {
              "detections": ...,
              "classes": ...
            }

Dabei dürfen Sie die Signalnamen "detections" und "classes" nicht verändern.

**Hinweis:**

Sie dürfen das Ultralytics (oder ein anderes geeignetes Model) zur Detektion der Spieler und des Balls verwenden. Mehr Informationen finden Sie [hier](https://docs.ultralytics.com/de/quickstart/#use-ultralytics-with-python).

Vortrainierte Gewichte für ein angepasstes YOLO-Netzwerk finden Sie [hier](https://drive.google.com/drive/folders/1AqfV35JcWXoxOOpAv8O_9wF57xmXbZVZ).


## Optischer Fluß
Die Aufgabe des optischen Flussmoduls besteht darin, die durchschnittliche Pixelverschiebung zwischen diesem und dem vorherigen Bild zu bestimmen.

Hinweis: Sie können auf data["image"] zugreifen, um das aktuelle Bild zu erhalten.

Geben Sie ein Python-Dictionary mit dem Bewegungsvektor zwischen diesem und dem vorherigen Bild zurück.

Das Signal "opticalFlow" muss ein 1x2-NumPy-Array enthalten, das die X- und Y-Verschiebung (Delta-Werte in Pixeln) des Bildbewegungsvektors angibt.

    return {
           "opticalFlow": ...
        }

Dabei dürfen Sie die Signalnamen "detections" und "classes" nicht verändern.

## Tracker
Die Aufgabe des Tracker-Moduls besteht darin, zeitlich konsistente Tracks aus der gegebenen Liste von Detektionen zu identifizieren.
Der Tracker verwaltet eine Liste bekannter Tracks, die anfangs leer ist.
Anschließend versucht der Tracker, alle vom Detektor gelieferten Erkennungen vorhandenen Spuren zuzuordnen.
Eine sinnvolle Metrik muss definiert werden, um zu entscheiden, welche Detekion welchem Track zugeordnet werden soll und welche Detektionen besser nicht zugewiesen werden.
Nach dem Zuordnungsschritt müssen drei verschiedene Fälle behandelt werden:
1) Detektionen, die keinem Track zugeordnet wurden:
Für diese wird eine neue Filterklasse erstellt, und ihr Zustand wird basierend auf der Erkennung initialisiert.
2) Tracks, die eine zugeordnete Detektion haben:
Der Zustand dieser Tracks kann basierend auf der zugeordneten Detektion aktualisiert werden.
3) Tracks, die keine zugeordnete Detektion haben:
Es ist sinnvoll, einige fehlende Frames zuzulassen, dennoch muss der aktuelle Zustand des Filters vorhergesagt werden
(z. B. basierend auf der Messung des optischen Flusses und der Objektgeschwindigkeit).
Falls zu viele Frames fehlen, kann der Track gelöscht werden.
Hinweis:

Sie können auf data["detections"] und data["classes"] zugreifen, um die aktuelle Liste der Erkennungen und deren zugehörige Klassen zu erhalten.

Sie müssen ein Wörterbuch mit den folgenden Feldern zurückgeben:
- "tracks": Ein Nx4-NumPy-Array, das einen 4-dimensionalen Zustandsvektor für jeden Track enthält.
Ähnlich wie bei den Erkennungen enthält der Spurzustand den Mittelpunkt (X, Y) sowie die Breite und Höhe der Begrenzungsbox (W, H).
- "trackVelocities": Ein Nx2-NumPy-Array mit einer zusätzlichen Geschwindigkeitsabschätzung (in Pixeln pro Frame) für jeden Track.
- "trackAge": Eine Nx1-Liste mit dem Alter jedem Trackr (Anzahl der Frames, die dieser Track existiert).
Das Alter beginnt bei der Erstellung der Spur bei 1 und erhöht sich monoton um 1 pro Frame, bis der Track gelöscht wird.
- "trackClasses": Eine Nx1-Liste der Klassen, die mit jedem Track verbunden sind.
Ähnlich wie bei den Detekionen muss die folgende Zuordnung verwendet werden:

      0: Ball
      1: Torhüter
      2: Spieler
      3: Schiedsrichter

- "trackIds": Eine Nx1-Liste eindeutiger IDs für jeden Track.
Die IDs dürfen nicht wiederverwendet werden und müssen während der gesamten Laufzeit des Programms eindeutig bleiben.

## Shirt Classifier
Die Aufgabe des Trikot-Klassifikationsmoduls besteht darin, die beiden Teams basierend auf ihrer Trikotfarbe zu identifizieren und jeden Spieler einem der beiden Teams zuzuweisen.

Hinweis:
Sie können auf data["image"] und data["tracks"] zugreifen, um das aktuelle Bild sowie die aktuelle Spurliste zu erhalten.
Sie müssen ein Wörterbuch mit den folgenden Feldern zurückgeben:

- "teamAColor": Ein 3-Tupel (B, G, R), das die Blau-, Grün- und Rot-Kanalwerte (zwischen 0 und 255) für Team A enthält.
- "teamBColor": Ein 3-Tupel (B, G, R), das die Blau-, Grün- und Rot-Kanalwerte (zwischen 0 und 255) für Team B enthält.
- "teamClasses": Eine Liste mit einer ganzzahligen Klassenzuordnung für jede Spur gemäß der folgenden Zuordnung:

      0: Team nicht entschieden oder kein Spieler (z. B. Ball, Torhüter, Schiedsrichter).
      1: Spieler gehört zu Team A.
      2: Spieler gehört zu Team B.

# Das Program
## Auswahl des Videos
Die Auswahl des abzuspielenden Videos passiert in der main.py Datei. Im unteren Abschnitt finden Sie die initiale Definition des Data-Dictionaries

    data = { "video": 'videos/2.mp4' }

Dort können Sie eines der 20 Videos eintragen welches dann abgespielt wird.

## Visualisierung
Die eingebaute Visualisierung erlaubt Ihnen ihre Ergebnisse (oder die von mir vorher aufgezeichneten) im Detail zu betrachten und zu analysieren. Dabei gibt es drei Visualisierungsmodi ("Detections", "Optical Flow" und "Tracks") welche sie durch drücken von jeweils "D", "O" oder "T" aktivieren können. Der jeweils aktive Modus wird oben in der Leiste grün hinterlegt angezeigt.

Während die Simulation beim Programmstart direkt läuft pausiert die Visualisierung zunächst. Sie können durch drücken der Leertaste ein einzelnes Bild nach vorne springen oder durch drücken von Enter die Simulation vorwärts ablaufen lassen. Alle prozessierten Bilder sowie alle dazugehörigen Ergebnisse werden von der Visualisierung in einem temporären Buffer gespeichert. Das erlaubt Ihnen durch drücken der "+" und "-" Taste vor- und zurück durch die Daten zu springen. Sie beenden das Programm durch drücken der Escape Taste. All diese Befehle finden sie zur Übersicht auch noch einmal im unteren Teil des Fensters. Ganz links sehen sie darüberhinaus auch die Bildnummer des aktuell angezeigten Bildes.
