import * as THREE from 'three';
import { ArcballControls } from 'three/addons/controls/ArcballControls.js';

const width = window.innerWidth, height = window.innerHeight;

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

	const material = new THREE.MeshNormalMaterial();
	const mesh = new THREE.Mesh( geometry, material );
	// Clear the scene of all but the initial children
	clear_mesh();
	scene.add( mesh );

	render()
}

function clear_mesh() {
	while(scene.children.length > num_initial_children){
		scene.remove(scene.children[num_initial_children]);
	}
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
