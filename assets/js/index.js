import * as THREE from 'three';
import { ArcballControls } from 'three/addons/controls/ArcballControls.js';

const width = parent.innerWidth * 0.78, height = parent.innerHeight * 0.9;

// init

const camera = new THREE.PerspectiveCamera( 50, width / height, 0.01, 1000 );
camera.position.z = 10;

const scene = new THREE.Scene();
scene.background = new THREE.Color( 0xcccccc );

const axesHelper = new THREE.AxesHelper( 5 );
scene.add( axesHelper );

const renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setSize( width, height );

const controls = new ArcballControls( camera, renderer.domElement, scene );
controls.addEventListener( 'change', function () {
	renderer.render( scene, camera );
} );
controls.update();

// Materials
const mesh_material = new THREE.MeshNormalMaterial( { transparent: true } );
const vertex_material = new THREE.MeshBasicMaterial( { color: 0x000000, transparent: true } );
setVertexOpacity(0);

window.addEventListener( 'resize', onWindowResize );
const num_initial_children = scene.children.length
animate();

export function addData( vertices, face_indices ) {
	document.getElementById("render-region").appendChild( renderer.domElement );

	const geometry = new THREE.BufferGeometry();
	geometry.computeVertexNormals()
	geometry.setAttribute( 'position', new THREE.BufferAttribute( new Float32Array(vertices), 3 )  );
	geometry.setIndex( face_indices );
	geometry.computeVertexNormals();

	const mesh = new THREE.Mesh( geometry, mesh_material );
	// set the mesh to be drawn last so it is above the transparent vertices
	mesh.renderOrder = -1
	// Clear the scene of all but the initial children
	clearMesh();
	scene.add( mesh );

	// addVertexMarkers( vertices );

	render()
}

function clearMesh() {
	while(scene.children.length > num_initial_children){
		scene.remove(scene.children[num_initial_children]);
	}
}

export function addVertexMarkers( vertices ) {
	// Vertices is a flat list of coordinates in the order [x1, y1, z1, x2, y2, z2, ...]
	for (let i = 0; i < vertices.length; i += 3) {
		const x = vertices[i];
		const y = vertices[i + 1];
		const z = vertices[i + 2];

		const sphereGeometry = new THREE.SphereGeometry(0.25, 6, 4);
		sphereGeometry.computeVertexNormals();
		sphereGeometry.translate(x, y, z)
		const vertex = new THREE.Mesh( sphereGeometry, vertex_material );
		scene.add( vertex );

	}
}

export function removeVertexMarkers() {
	while(scene.children.length > num_initial_children + 1){
		scene.remove(scene.children[num_initial_children + 1]);
	}
}

export function setMeshOpacity( value ) {
	mesh_material.opacity = value;
	render();
}

export function setVertexOpacity( value ) {
	vertex_material.opacity = value;
	render();
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
