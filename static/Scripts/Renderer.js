import * as THREE from 'https://cdn.jsdelivr.net/npm/three@latest/build/three.module.js';

const scene = new THREE.Scene(); // Set up scene.
const camera = new THREE.PerspectiveCamera( 120, window.innerWidth / window.innerHeight, 0.1, 1000 );
scene.background = new THREE.Color( 0xffffff ); // Set background color.
const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );


// Render a Cube.
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshPhongMaterial( { color: 0x44aa88} );
const cube = new THREE.Mesh( geometry, material );
// scene.add( cube );
camera.position.z = 5;

const sphere = new THREE.SphereGeometry(1.4, 4096, 4096);
const sphereMaterial = new THREE.MeshPhongMaterial({ color: 0xff0000 });
sphereMaterial.shininess = 100;
sphereMaterial.specular = new THREE.Color(0x222222);
sphereMaterial.flatShading = false;
sphereMaterial.side = THREE.DoubleSide;
sphereMaterial.transparent = false;
sphereMaterial.opacity = 1.0;

const sphereMesh = new THREE.Mesh(sphere, sphereMaterial);
sphereMesh.position.set(2, 0, 0);
scene.add(sphereMesh);

const Circlegeometry = new THREE.CircleGeometry( 5, 256);
const circlematerial = new THREE.MeshBasicMaterial( { color: 0xffff00 } );
const circle = new THREE.Mesh( Circlegeometry, circlematerial );
scene.add( circle )
// const DiscMesh = new THREE.Mesh(Circlegeometry, circlematerial);
// DiscMesh.position.set(2, 0, 0);
// scene.add(DiscMesh)

// Render Light.
const light = new THREE.DirectionalLight( 0xffffff, 1 );
light.position.set( 5, 5, 5 );
light.castShadow = true;
light.specular = new THREE.Color(0xaaaaaa);
light.color = new THREE.Color(0xffffff);
light.intensity = 1;
scene.add( light );




// Maintain the Animation Loop.
function animate(time) {
    time *= 0.001;  // convert time to seconds
    // cube.rotation.x += 0.01;
    // cube.rotation.y += 0.01;
    // cube.rotation.z += 0.09;
    
    sphereMesh.castShadow = true;
    sphereMesh.receiveShadow = true;
    sphereMesh.position.x = 2 * Math.cos(3 * time);
    circle.rotation.x += 0.1;
    circle.rotation.z += 0.1;
    circle.receiveShadow = true;
    circle.castShadow = true;
    circle.position.x = 2 * Math.cos(3 * time);
    

    light.castShadow = true;
    light.shadow.mapSize.width = 512; // default
    light.shadow.mapSize.height = 512; // default
    light.shadow.camera.near = 0.5; // default
    light.shadow.camera.far = 500; // default
    light.shadow.bias = -0.0001;
    light.shadow.radius = 1;
    light.shadow.camera.left = -10;
    light.shadow.camera.right = 10;
    light.shadow.camera.top = 10;
    light.shadow.camera.bottom = -10;
    renderer.render( scene, camera );
}
renderer.setAnimationLoop( animate );

