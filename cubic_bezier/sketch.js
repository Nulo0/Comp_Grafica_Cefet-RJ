let pontos = [];
let selecionado = null;

function setup() {
    createCanvas(600,600);
    pontos = [
        createVector(50,height/2), 
        createVector(25,height/8), 
        createVector(375,height/8),
        createVector(width - 10, height/2)
    ];
}  

function ponto(A) {
    circle(A.x,A.y,10);
}

function combina(A,B,t) {
    return {x:(1-t)*A.x+t*B.x,y:(1-t)*A.y+t*B.y};
}

function draw() {
    let [p1, p2, p3, p4] = pontos;
    background(200);
    noFill();
    beginShape();
    for(let t=0; t<=1.0; t+=0.05) {
        A = combina(p1,p2,t);
        B = combina(p2,p3,t);
        C = combina(p3, p4, t);
        D = combina(A, B, t);
        E = combina(B, C, t);
        F = combina(D, E, t);
        vertex(F.x,F.y);
    }
    endShape();
    desenhaPontos();
}

function desenhaPontos() {
    let vmouse = createVector(mouseX,mouseY);
    selecionado = null;
    for(let p of pontos) {
        if(vmouse.dist(p)<10) {
            selecionado = p;
            fill("#ff0000");
        } else {
            fill("#ffffff");
        }
        ponto(p);
    }
}

function mouseDragged() {
    if(selecionado) {
        selecionado.set(mouseX, mouseY);
    }
}
