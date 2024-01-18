import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const width = window.innerWidth, height = window.innerHeight;

// init

const camera = new THREE.PerspectiveCamera( 50, width / height, 0.01, 1000 );
camera.position.z = 10;

const scene = new THREE.Scene();
scene.background = new THREE.Color( 0xcccccc );

const axesHelper = new THREE.AxesHelper( 5 );
scene.add( axesHelper );

let mesh = new THREE.Mesh();

const renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setSize( width, height );

const controls = new OrbitControls( camera, renderer.domElement );

controls.listenToKeyEvents( window )
controls.update();
controls.enableDamping = true; // an animation loop is required when either damping or auto-rotation are enabled
controls.dampingFactor = 0.05;

controls.screenSpacePanning = false;

controls.minDistance = 1;
controls.maxDistance = 500;

// controls.maxPolarAngle = Math.PI / 2;

window.addEventListener( 'resize', onWindowResize );
animate();

export function addData( vertices, face_indices ) {
	document.getElementById("render-region").appendChild( renderer.domElement );

	const geometry = new THREE.BufferGeometry();
	geometry.computeVertexNormals()
	geometry.setAttribute( 'position', new THREE.BufferAttribute( new Float32Array(vertices), 3 )  );
	geometry.setIndex( face_indices );
	geometry.computeVertexNormals();

	const material = new THREE.MeshNormalMaterial();
	mesh = new THREE.Mesh( geometry, material );
	scene.add( mesh );

	render()
}

function onWindowResize() {

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	controls.handleResize();

	renderer.setSize( window.innerWidth, window.innerHeight );

}

function animate() {

	requestAnimationFrame( animate );

	controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true

	render();

}

function render() {

	renderer.render( scene, camera );

}
