import os

def get_bullet_includes(BULLET_DIRECTORY):
    return [
        # General
        os.path.join(BULLET_DIRECTORY, 'src', 'btBulletCollisionCommon.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'btBulletDynamicsCommon.h'),
        # Linear Math
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btVector3.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btQuadWord.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btQuaternion.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btMatrix3x3.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btTransform.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath', 'btMotionState.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'LinearMath',
                     'btDefaultMotionState.h'),
        # Bullet Collision
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btCollisionShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btBoxShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btSphereShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btCapsuleShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btCylinderShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btConeShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btStaticPlaneShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btConvexHullShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btTriangleMesh.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btConvexTriangleMeshShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btBvhTriangleMeshShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btScaledBvhTriangleMeshShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btTriangleMeshShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btTriangleIndexVertexArray.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btCompoundShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btTetrahedronShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btEmptyShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btMultiSphereShape.h'),
        os.path.join(BULLET_DIRECTORY, 'src', 'BulletCollision',
                     'CollisionShapes', 'btUniformScalingShape.h'),
    ]

def get_idl_file_paths(ROOT):
    return [
        os.path.join(ROOT, 'data', 'idls', 'linear-math.idl'),
        os.path.join(ROOT, 'data', 'idls', 'bullet-collision.idl'),
    ]
