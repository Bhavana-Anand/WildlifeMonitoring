/*#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "LA2_22BCT0213.h"

#define NUM_READINGS 1200

int main() {
    // Initialize random seed
    srand(time(NULL));
    
    // Open CSV file for writing
    FILE *file = fopen("optics1.csv", "w");
    if (file == NULL) {
        printf("Error opening file!\n");
        return 1;
    }
    
    // Write CSV header
    fprintf(file, "Reading,Quantum_Efficiency,Photon_Flux,Photocurrent\n");
    
    // Generate and save 100 readings
    for (int i = 0; i < NUM_READINGS; i++) {
        // Generate random values
        double eta = generate_quantum_efficiency();
        double phi = generate_photon_flux();
        
        // Calculate photocurrent
        double current = calculate_photocurrent(eta, phi);
        
        // Write to CSV file
        fprintf(file, "%d,%.6f,%.6e,%.6e\n", i+1, eta, phi, current);
        
        // Print every 10th reading to console for monitoring
        if ((i + 1) % 10 == 0) {
            printf("Completed %d readings...\n", i + 1);
        }
    }
    
    // Close file
    fclose(file);
    
    printf("\nAll readings completed and saved to 'photoelectric_readings.csv'\n");
    
    // Print first 5 readings from the file for verification
   /* printf("\nFirst 5 readings from the file:\n");
    file = fopen("photoelectric_readings.csv", "r");
    if (file != NULL) {
        char line[256];
        int count = 0;
        
        // Skip header
        fgets(line, sizeof(line), file);
        
        // Print first 5 lines
        while (fgets(line, sizeof(line), file) != NULL && count < 5) {
            printf("%s", line);
            count++;
        }
        fclose(file);
    }*/
    
    /*return 0;
}*/

/*#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h> // For sleep()
#include "la2_22bct0213.h"
//#include "afir sensor.h"
#define GRID_SIZE 10
#define NUM_ANIMALS 5
int main() 
{
    srand(time(NULL)); // Seed random generator
    // Initialize animals
    Animal animals [NUM_ANIMALS]; 
    for (int i = 0; i < NUM_ANIMALS; i++) 
    { 
        animals[i].id = i+1; 
        animals[i].x = rand() % GRID_SIZE; 
        animals[1].y = rand() % GRID_SIZE; 
        animals[i].heat_signature = 36.0; 
    }
    // Open file for writing sensor data
    FILE *file;
    printf("\nWildlife & Fire Monitoring System\n");
    for (int step; step < 50; step++) { // Run for 50 iterations
        file = fopen("sensor_data.csv", "w"); 
        if (file == NULL) {
            perror("Error opening file");
            return 1;
    }
    fprintf(file, "Step: %d\n", step + 1);
    // Fire detection
    for (int x = 0; x < GRID_SIZE; x++) {
        for(int y=0;y<GRID_SIZE;y++)
    float temp = get_temperature(x, y); if (detect_fire(temp)) {
    fprintf(file, "FIRE %d %d %.2f\n", x, y, temp);
    }
    }
    }
    }*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "LA2_22BCT0213.h"

int main() {
    MonitoringSystem system;
    char alert_message[200];
    int frame;
        
        // Initialize the system
        initializeSystem(&system);
        printf("Wildlife Monitoring System initialized\n");
        printf("Tracking %d deer with heat signature of %.1f°C\n", 
               system.deer_count, system.deer_heat_signature);
        
        // Main simulation loop
        for (frame = 0; frame < 100; frame++) {
            // Update temperature grid with diffusion
            updateTemperatureGrid(&system);
            
            // Randomly start new fires
            startFire(&system);
            
            // Update existing fires
            updateFires(&system);
            
            // Update deer positions
            updateAnimals(&system);
            
            // Update animal grid
            updateAnimalGrid(&system);
            
            // Generate alerts
            generateAlert(&system, alert_message, sizeof(alert_message));
            
            // Print current system state
            printSystemState(&system);
            
            // Save heatmaps to files (optional, for external visualization)
            if (frame % 10 == 0) {
                char temp_filename[50], animal_filename[50];
                sprintf(temp_filename, "temperature_grid_%03d.dat", frame);
                sprintf(animal_filename, "animal_grid_%03d.dat", frame);
                
                saveHeatmapToFile(system.temperature_grid, temp_filename);
                saveHeatmapToFile(system.animal_grid, animal_filename);
            }
            
            // Sleep code removed
        }
        
        printf("Simulation complete\n");
        return 0;
    }