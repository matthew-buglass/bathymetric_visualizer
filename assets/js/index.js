import THREE from "three";

const width = window.innerWidth, height = window.innerHeight;

// init

const camera = new THREE.PerspectiveCamera( 100, width / height, 0.01, 100 );
camera.position.z = 10;

const scene = new THREE.Scene();
let mesh = new THREE.Mesh();

const renderer = new THREE.WebGLRenderer( { antialias: true } );
renderer.setSize( width, height );
document.getElementById("render-region").appendChild( renderer.domElement );

// const controls = new OrbitControls( camera, renderer.domElement );
// controls.target.set( 0, 0.5, 0 );
// controls.update();
// controls.enablePan = false;
// controls.enableDamping = true;

function add_data( vertices, face_indices ) {
	const geometry = new THREE.BufferGeometry();
	geometry.computeVertexNormals()
	geometry.setAttribute( 'position', new THREE.BufferAttribute( new Float32Array(vertices), 3 )  );
	geometry.setIndex( face_indices );
	geometry.computeVertexNormals();

	const material = new THREE.MeshNormalMaterial();
	mesh = new THREE.Mesh( geometry, material );
	scene.add( mesh );
	renderer.render( scene, camera );
}
