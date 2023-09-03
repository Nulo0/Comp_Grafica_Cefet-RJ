let radius = 250; // Definindo raio do círculo como 250
let numPoints = 60; //Definindo o numero de pontos ou marcações no círculo, vão ser usadso para representar os segundos e os risquinhos do relogio

// Coordenadas que vão ser usadas para desenhar os ponteiros
let px = 0; 
let py = 0;

// Variávies pra armazenar as horas e os outros
let h, m, s;

// Iniciliza as variaveis para os raios coorespondentes
let segRadius, minRadius, horaRadius;

function setup() {
    createCanvas(900, 700);

    segRadius = radius * 0.9;
    minRadius = radius * 0.7;
    horaRadius = radius * 0.5;
}

function draw() {
    background(220);
    translate(width / 2, height / 2);

    strokeWeight(8);  // Espessura das circulo
    stroke(0); // Deixar circulo preto
    noFill(); // Deixar circulo sem preenchimento
    circle(0, 0, radius * 2); // Criando circulo

    strokeWeight(8);  // Pontinho no centro do circulo
    point(0, 0);

    for (let i = 0; i < numPoints; i++) {
        let angle = map(i, 0, numPoints, -HALF_PI, TWO_PI - HALF_PI);
        let x = radius * cos(angle);
        let y = radius * sin(angle);
        
        stroke(0);
        if (i % 5 === 0) {
            strokeWeight(4)
            line(x * 0.8, y * 0.8, x, y);
            let num = i === 0 ? 12 : i / 5;
            fill(0);
            noStroke()
            textSize(24);
            textAlign(CENTER, CENTER);
            text(num, x * 1.1, y * 1.1);
        } else {
            strokeWeight(4)
            line(x * 0.9, y * 0.9, x, y);
        }
    }

    s = second();
    m = minute() + s / 60;
    h = hour() % 12 + m / 60;

    drawPointer(s, segRadius, 60, 'red');
    drawPointer(m, minRadius, 60, 'blue');
    drawPointer(h, horaRadius, 12, 'green');
}

function drawPointer(value, pointerRadius, divisions, color) {
    let angle = map(value, 0, divisions, -HALF_PI, TWO_PI - HALF_PI);

    px = pointerRadius * cos(angle);
    py = pointerRadius * sin(angle);

    stroke(color);
    strokeWeight(4);  // Espessura do ponteiro fino
    line(0, 0, px, py);
}
